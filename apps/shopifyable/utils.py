import urllib
import urllib2
import urlparse
import inspect
from dateutil.parser import parse

__all__ = ['generate_url', 'generate_request', 'parse_xml', 'serialize_xml']

def _import_etree(packages=('lxml.etree', 'xml.etree.cElementTree',
                            'cElementTree', 'elementtree.ElementTree')):
    for pkg_name in packages:
        try:
            pkg = __import__(pkg_name)
        except ImportError:
            continue
        else:
            for subpkg_name in pkg_name.split('.')[1:]:  # skip the base package
                assert hasattr(pkg, subpkg_name)
                pkg = getattr(pkg, subpkg_name)
            return pkg
    raise ImportError("ElementTree library could not be found")

etree = _import_etree()
etree_element = type(etree.Element('example'))  # etree.Element is a factory

def generate_url(protocol, domain, path, param_dict):
    url = "%s://%s%s" % (protocol, domain, path)
    if len(param_dict) > 0:
        return urlparse.urljoin(url, '?' + urllib.urlencode(param_dict))
    else:
        return url

def generate_request(action, url, body=None):
    assert action.upper() in ('GET', 'DELETE') and body is None or \
           action.upper() in ('POST', 'PUT')

    request = urllib2.Request(url, data=body)
    request.get_method = lambda: action
    return request

def parse_xml(obj):
    return etree.parse(obj).getroot()

def serialize_xml(obj):
    return etree.tostring(obj)
  
def format_datetime(dt):
    s = dt.strftime("%Y-%m-%dT%H:%M")
    tz = dt.utcoffset()
    return "{0:%Y-%m-%dT%H:%M}{1:0=+3}:{2:0=2}".format(dt, tz.hour, tz.minute)
    
def lookup_kwargs(klass, element):
    for key, value in klass.Shopify.shopify_fields.iteritems():
        if value == 'id':
            return { 'id': element.find(key).text }
    return None
    
def parse_element(element, key):
    field_tag = None
    
    # print element
    # print key
    # import ipdb; ipdb.set_trace()
    
    try:
        element_type = element.find(key).attrib['type']
        if element_type == 'datetime':
            field_value = parse(element.find(key).text) if element.find(key).text else None
        if element_type == 'boolean':
            field_value = element.find(key).text.capitalize()
        if element_type == 'decimal':
            field_value = float(element.find(key).text) if element.find(key).text else None
        if element_type == 'integer':
            field_value = int(element.find(key).text) if element.find(key).text else None
        if element_type == 'array':
            field_value = None 
            field_tag = element.tag
            
    except KeyError, e:
        element_type = None
        field_value = element.find(key).text
        
    except AttributeError, e:
        
        if len(element):
            """
            If we are here, we have an element with children that
            is not an type=array
            """
            element_type = 'dict' # assign it a dict type for our use
            field_value = None
            field_tag = element.tag
        else:
            element_type = None
            try:
                field_value = element.find(key).text
            except:
                field_value = None
            field_tag = element.tag
    return element_type, field_value, field_tag
    
def sub_element_kwargs_list(klass, element, element_type):
    """
    Recurse through the child sub-element and return
    a [] of {}'s assigned to the klass as the key, i.e.
    klass: [{...}, {...}, {...}]
    """
    # kwargs = {}
    obj_kwargs_list = []
    
    if element_type == 'array':
        """
        Try to get the child elements, we might be dealing children w/ children
        or just children themselves
        """
        sub_elements = list(element)
        for sub_element in sub_elements:
            obj_kwargs = {}
        
            for key, value in klass.Shopify.shopify_fields.iteritems():
                element_type, field_value, field_tag = parse_element(sub_element, key)
                field_key = value
                obj_kwargs.update({ field_key: field_value })

    elif element_type == 'dict':

        sub_elements = element.getchildren()

        for sub_element in sub_elements:
            
            obj_kwargs = {}
            element_type, field_value, field_tag = parse_element(sub_element, sub_element.tag)
            field_key = sub_element.tag
            obj_kwargs.update({ field_key: field_value })
            
        obj_kwargs_list.append(obj_kwargs)
    
    # kwargs.update({klass:obj_kwargs_list})    
    return obj_kwargs_list
    
def element_kwargs(klass, element):
    
    kwargs = {}
    
    for key, value in klass.Shopify.shopify_fields.iteritems():
        """
        Loop through the model's Shopify.shopify_fields that
        serve as a map for the API's xml elements.
        """
        
        element_type, field_value, field_tag = parse_element(element, key)
        field_key = value
        
        if element_type == 'array':
            """
            If the element type is 'array' then traverse
            into the child elements, building a list
            of {}'s assigned to the klass, for later
            recursing
            """
            obj_dict_list = []
            
            if klass.Shopify.shopify_arrays:
                
                for k, v in klass.Shopify.shopify_arrays.iteritems():
                    if inspect.isclass(v):
                        obj_dict_list = sub_element_kwargs_list(v, element.find(k), element_type)
                        kwargs.update({v: obj_dict_list})
                        
        elif element_type == 'dict':
            """
            If the element type is 'dict', then
            we should pull out the child elements and 
            build a singular {} -- almost the same as
            element_type == 'array'
            """
            if klass.Shopify.shopify_dicts:
                
                for k, v in klass.Shopify.shopify_dicts.iteritems():
                    if inspect.isclass(v):
                        obj_dict_list = sub_element_kwargs_list(v, element.find(k), element_type)
                        kwargs.update({v: obj_dict_list})
            
        else:
            kwargs.update({ field_key: field_value })
    
    return kwargs
    
def etree_kwargs(klass, etree):
    kwargs_list = []
    for element in list(etree):
        kwargs_list.append(element_kwargs(klass, element))
    return kwargs_list

