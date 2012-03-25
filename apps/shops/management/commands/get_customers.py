from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from shopifyable.utils import parse_shop_object
from shops.models import Shop
from customers.models import Customer


def fetch_customers(shop):
    
    shop.customers()
    
    for _customer in (shop._customers):
        
        customers = parse_shop_object(shop, Customer, _customer)
        
    return customers
        

class Command(BaseCommand):
    help = 'collect customers from shopify and place in the Customer model'

    def handle(self, *args, **options):
        """
        Customers
        """

        shops = Shop.objects.all()
        
        for shop in shops:
            shop.connect()
            fetch_customers(shop)

        