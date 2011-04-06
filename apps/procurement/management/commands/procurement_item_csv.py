from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from procurement.models import ProcurementItem
from procurement.utils import procurement_item_defaults

import ipdb

class Command(BaseCommand):
    help = 'process procurement orders'

    def handle(self, *args, **options):
        """
        Procurement Items CSV
        """
        
        order_by_args = [
            'product_variant__product__vendor', 
            'product_variant', ]
        
        procurement_items = ProcurementItem.objects.all().order_by(*order_by_args)
        
        for procurement_item in procurement_items:
            print ', '.join([
                procurement_item.product_variant.product.vendor,
                str(procurement_item.product_variant.product),
                str(procurement_item.product_variant),
                str((procurement_item.order_units) or ''),
                str((procurement_item.order_weight) or '')])
            