import urllib
import urllib2
import urlparse

from pytz import timezone

from dateutil.parser import parse

from django.conf import settings
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import get_model
from django.utils import simplejson

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

def _decode_dict(dct):
    """
    Turn the dictionary keys into strings for Django ORM
    """
    newdict = {}
    for k, v in dct.iteritems():
        if isinstance(k, unicode):
            k = k.encode('utf-8')
        newdict[k] = v
    return newdict

def parse_json(obj):
    return simplejson.load(obj, object_hook=_decode_dict)

def format_datetime(dt):
    s = dt.strftime("%Y-%m-%dT%H:%M")
    tz = dt.utcoffset()
    return "{0:%Y-%m-%dT%H:%M}{1:0=+3}:{2:0=2}".format(dt, tz.hour, tz.minute)

def lookup_kwargs(klass, element):
    for key, value in klass.Shopify.shopify_fields.iteritems():
        if value == 'id':
            return { 'id': element.find(key).text }
    return None

def resolve_relation(relation):

    # Look for an "app.Model" relation
    try:
        app_label, model_name = relation.split(".")
    except ValueError:
        # If we can't split, assume a model in current app
        # app_label = cls._meta.app_label
        # model_name = relation
        pass
    except AttributeError:
        # If it doesn't have a split it's actually a model class
        app_label = relation._meta.app_label
        model_name = relation._meta.object_name

    return get_model(app_label, model_name, False)

def _parse_rel_objs(rel_objs, rel_klass, rel_obj_json):

    rel_obj_dict = {}

    if hasattr(rel_klass, 'Shopify'):
        if hasattr(rel_klass.Shopify, 'shopify_fields'):
            fields_dict = rel_klass.Shopify.shopify_fields
            for k, v in fields_dict.iteritems():
                rel_obj_dict.update({ fields_dict[k]: rel_obj_json[k] })

            
            if hasattr(rel_klass.Shopify, 'shopify_date_fields'):
                date_fields = rel_klass.Shopify.shopify_date_fields
                for key, value in date_fields.iteritems():
                    if key in rel_klass.Shopify.shopify_date_fields:
                        if value is not None:
                            #print value
                            #import ipdb; ipdb.set_trace()
                            rel_obj_dict.update({ key: parse(rel_obj_json[value]) })

            rel_obj = rel_klass(**rel_obj_dict)
            rel_objs.append(rel_obj)
            del(rel_obj)

    return rel_objs

def parse_shop_object(shop, klass, obj_json, sync=False):
    """
        if sync=True

        compare the updated_at datetime, and which ever is more recent
        then change.
    """
    
    obj_dict = {}
    rel_objs = []

    if hasattr(klass, 'Shopify'):

        for key, value in obj_json.iteritems():

            if hasattr(klass.Shopify, 'shopify_dicts'):
                if key in klass.Shopify.shopify_dicts:
                    rel_klass = resolve_relation(klass.Shopify.shopify_dicts[key])
                    rel_obj_json = value
                    rel_objs = _parse_rel_objs(rel_objs, rel_klass, rel_obj_json)

            if hasattr(klass.Shopify, 'shopify_arrays'):
                if key in klass.Shopify.shopify_arrays:
                    rel_klass = resolve_relation(klass.Shopify.shopify_arrays[key])
                    for rel_obj_json in obj_json[key]:
                        rel_objs = _parse_rel_objs(rel_objs, rel_klass, rel_obj_json)

            if hasattr(klass.Shopify, 'shopify_fields'):
                if key in klass.Shopify.shopify_fields:
                    obj_dict.update({ key: value })

                    if key == 'shopify_product_variant_id':
                        pass

            if hasattr(klass.Shopify, 'shopify_date_fields'):
                if key in klass.Shopify.shopify_date_fields:
                    if value is not None:                
                        obj_dict.update({ key: parse(value) })
                    
        try:
            obj = klass(**obj_dict)
            obj.shop = shop
        except TypeError, e:
            import ipdb; ipdb.set_trace()

        db_obj = None

        try:
            # Get a database entry based on the obj
            db_obj = klass.objects.get(id=obj.id)
        except MultipleObjectsReturned:
            pass
        except ObjectDoesNotExist:
            pass

        # Save object if it doesn't exist or has no updated_at time
        if (db_obj is None) or (obj.updated_at is None) \
            or (db_obj.updated_at is None):
            print obj, ": Doesn't exist, creating new object"

            obj.save()
        else: # Update object if the date is different
            # TODO: Convert into local timezone if possible

            # Remove timezone information for date comparison
            obj.updated_at = obj.updated_at.replace(tzinfo=None)
            db_obj.updated_at = db_obj.updated_at.replace(tzinfo=None)
                
            print '(%s): Server: %s, Ours: %s' % (obj, obj.updated_at, db_obj.updated_at)
            # If date is different, update the object
            
            if obj.updated_at != db_obj.updated_at:
               obj.save()
               print "Updated object"
               
        for rel_obj in rel_objs:
            """
            Set the value of the rel_obj.parent_obj
            """
            setattr(rel_obj, obj._meta.module_name, obj)
            try:
                rel_obj.full_clean()
            except ValidationError, e:
                print e

                if hasattr(rel_obj, 'updated_at'):
                    
                    try:
                        test_obj = rel_obj.__class__.objects.get(id=rel_obj.id)
                    except ObjectDoesNotExist:
                        pass
                    else:
                        rel_obj.updated_at = rel_obj.updated_at.replace(tzinfo=None)
                        test_obj.updated_at = test_obj.updated_at.replace(tzinfo=None)
                        if rel_obj.updated_at != test_obj.updated_at:
                            print "rel_obj updated"
                            rel_obj.save() # replaces the test_obj?
                            continue
            else:
                try:
                    # Save object if it doesn't exist or has no update_at time
                            
                    if (db_obj is None) or (obj.updated_at is None) \
                        or (db_obj.updated_at is None):
                        rel_obj.save()
                        print "Created rel obj:  %s" % rel_obj 
                    else: # Update object if the date is different
                        if (db_obj.updated_at != obj.updated_at):
                            rel_obj.save()
                            print "Updated rel obj: %s" % rel_obj
                        else:
                            print "Rel obj not changed: %s" % rel_obj                

                except Exception, e:
                    print e

    return obj

def parse_shop_objects(shop, klass, objs_json):
    objs = []
    for obj_json in objs_json:
        objs.append(parse_shop_object(shop, klass, obj_json))
    return objs
