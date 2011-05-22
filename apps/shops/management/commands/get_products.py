from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from shopifyable.utils import element_kwargs
from shops.models import Shop
from products.models import Product, ProductVariant

import inspect
import ipdb

def fetch_products(shop):
    
    shop.products()
    for _product in (shop._products):
        
        product_dict = element_kwargs(Product, _product)
        related_objs = []
        for key, value in product_dict.iteritems():
            if inspect.isclass(key) and issubclass(ProductVariant, key) and not value is None:
                obj_dicts = value
                obj_class = ProductVariant
                for obj_dict in obj_dicts:
                    obj = obj_class(**obj_dict)
                    related_objs.append(obj)
                product_dict.pop(key)
                break
        
        product = Product(**product_dict)
        product.shop = shop
        product.save()
        print product
        for obj in related_objs:
            obj.product = product
            obj.save()
            print u'    %s' % obj
            
        

class Command(BaseCommand):
    help = 'collect products from shopify and place in the Product model'

    def handle(self, *args, **options):
        """
        Products
        """

        shops = Shop.objects.all()
        
        for shop in shops:
            shop.connect()
            fetch_products(shop)

        