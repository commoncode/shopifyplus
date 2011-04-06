from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from procurement.models import ProcurementItem
from procurement.utils import procurement_item_defaults

import ipdb
            

class Command(BaseCommand):
    help = 'process procurement orders'

    def handle(self, *args, **options):
        """
        Process Procurement Orders
        """
        
        procurement_items = ProcurementItem.objects.all()
        procurement_item_defaults(procurement_items)
        