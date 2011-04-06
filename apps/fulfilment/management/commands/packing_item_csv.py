from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from fulfilment.utils import packing_item_csv
from fulfilment.models import PackingItem


import ipdb
            

class Command(BaseCommand):
    help = 'process packing items'

    def handle(self, *args, **options):
        """
        Process Packing Items to CSV
        """

        packing_items = PackingItem.objects.all()
        packing_item_csv(packing_items)



