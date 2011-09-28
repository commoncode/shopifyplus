import inspect
import dateutil.parser as dateparser
import datetime

from django.core.exceptions import ValidationError

from shopifyable.utils import resolve_relation

from ordering.models import Order, OrderItem, ShippingLine, ShippingAddress, BillingAddress

def fetch_orders(shops):
    
    orders = []
    
    for shop in shops:
        shop.orders()
        for _order in (shop._orders):
            
            order_dict = _order
            
            obj_dict = {}
            rel_objs = []
            for key, value in order_dict.iteritems():
                
                if key in Order.Shopify.shopify_dicts:
                    klass = resolve_relation(Order.Shopify.shopify_dicts[key])
                    rel_obj_dict = {}
                    for k, v in klass.Shopify.shopify_fields.iteritems():
                        rel_obj_dict.update({ k: value[k] })
                    rel_obj = klass(**rel_obj_dict)
                    rel_objs.append(rel_obj)
                    del(rel_obj)
                        
                if key in Order.Shopify.shopify_arrays:
                    klass = resolve_relation(Order.Shopify.shopify_arrays[key])
                    
                    for _item in _order[key]:
                        rel_obj_dict = {}
                        for k, v in klass.Shopify.shopify_fields.iteritems():
                            rel_obj_dict.update({ k: _item[k] })
                        rel_obj = klass(**rel_obj_dict)
                        rel_objs.append(rel_obj)
                        del(rel_obj)
                        
                if key in Order.Shopify.shopify_fields:
                    obj_dict.update({ key: value })
                    
                if key in Order.Shopify.shopify_date_fields:
                    try:
                        obj_dict.update({ key: dateparser.parse(value) })
                    except:
                        pass
                        
            obj = Order(**obj_dict)
            obj.shop = shop
            obj.save()
            print u'%s' % obj
            
            for rel_obj in rel_objs:
                rel_obj.order = obj
                try:
                    rel_obj.full_clean()
                except ValidationError, e:
                    print e
                else:
                    rel_obj.save()
                    print u'    %s' % rel_obj
            
            orders.append(obj)
    
    return orders