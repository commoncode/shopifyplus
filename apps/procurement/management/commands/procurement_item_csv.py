from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from procurement.models import ProcurementItem, Procurement
from procurement.utils import procurement_item_defaults

class Command(BaseCommand):
    help = 'process procurement orders'

    def handle(self, *args, **options):
        """
        Procurement Items CSV
        """
        
        for procurement in Procurement.objects.all():
        
            order_by_args = [
                'product_variant__product__vendor', 
                'product_variant', ]
        
            procurement_items = procurement.procurementitem_set.all().order_by(*order_by_args)
            # ProcurementItem.objects.all().order_by(*order_by_args)
            
            print u'===== Procurement CSV :: START ======'
            for procurement_item in procurement_items:
                try:
		    print '; '.join([
                        procurement_item.product_variant.product.vendor,
                        str(procurement_item.product_variant.product),
                        str(procurement_item.product_variant),
                        str((procurement_item.order_units) or ''),
                        str((procurement_item.order_weight) or '')])
                except:
                    print u'%s; %s; ; ; ' % (procurement_item.product_variant.product.vendor, str(procurement_item.product_variant.product))
                print u'===== Procurement CSV :: END ======'
            
