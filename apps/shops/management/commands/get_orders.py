from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from shops.models import Shop

from shops.utils import fetch_orders

class Command(BaseCommand):
    help = 'collect orders from shopify and place in the Order model'

    def handle(self, *args, **options):
        """
        Orders
        """
        
        shops = Shop.objects.all()
        
        fetch_orders(shops)
        