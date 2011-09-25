import inspect

from shopifyable.utils import element_kwargs

from ordering.models import Order, OrderItem, ShippingLine, ShippingAddress, BillingAddress

def fetch_orders(shops):
    
    orders = []
    
    for shop in shops:
        shop.orders()
        for _order in (shop._orders):
            
            order_dict = element_kwargs(Order, _order)
            
            related_objs = []
            keys = []
            for key, value in order_dict.iteritems():
                
                if inspect.isclass(key):
                    if issubclass(OrderItem, key):
                        klass = OrderItem
                    elif issubclass(ShippingLine, key):
                        klass = ShippingLine
                    elif issubclass(ShippingAddress, key):
                        klass = ShippingAddress
                    elif issubclass(BillingAddress, key):
                        klass = BillingAddress
                        
                    obj_dicts = value
                    obj_class = klass
                    for obj_dict in obj_dicts:
                        try:
                            obj = obj_class(**obj_dict)
                        except TypeError, e:
                            print e
                            print obj_class
                        else:
                            related_objs.append(obj)
                            
                    keys.append(key)
                    
            for key in keys:
                order_dict.pop(key)
            
            order = Order(**order_dict)
            order.shop = shop
            order.save()
            print order
            for obj in related_objs:
                obj.order = order
                obj.save()
                print u'    %s' % obj
            
            orders.append(order)
    
    return orders