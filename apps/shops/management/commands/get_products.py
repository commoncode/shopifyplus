from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from shopifyable.utils import parse_shop_object
from shops.models import Shop
from products.models import Product


def fetch_products(shop):
    
    shop.products()
    
    for _product in (shop._products):
        
        products = parse_shop_object(shop, Product, _product)
        
    return products
        

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

        