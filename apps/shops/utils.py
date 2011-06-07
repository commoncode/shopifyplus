import inspect

from shopifyable.utils import element_kwargs

from ordering.models import Order, OrderItem

def fetch_orders(shops):
    
    orders = []
    
    for shop in shops:
        shop.orders()
        for _order in (shop._orders):
        
            order_dict = element_kwargs(Order, _order)
        
            related_objs = []
            for key, value in order_dict.iteritems():
                if inspect.isclass(key) and issubclass(OrderItem, key):
                    obj_dicts = value
                    obj_class = OrderItem
                    for obj_dict in obj_dicts:
                        obj = obj_class(**obj_dict)
                        related_objs.append(obj)
                    order_dict.pop(key)
                    break
        
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