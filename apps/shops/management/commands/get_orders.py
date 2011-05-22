from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from shopifyable.utils import element_kwargs
from shops.models import Shop
from ordering.models import Order, OrderItem

import inspect
import ipdb


def fetch_orders(shop):
    
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
            

class Command(BaseCommand):
    help = 'collect orders from shopify and place in the Order model'

    def handle(self, *args, **options):
        """
        Orders
        """
        
        shops = Shop.objects.all()

        for shop in shops:
            shop.connect()
            fetch_orders(shop)
        