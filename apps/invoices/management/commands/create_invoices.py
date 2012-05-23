from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from fulfilment.models import Packing
from invoices.utils import process_packings, create_invoices
from invoices.models import Invoice



class Command(BaseCommand):
    help = 'process packings to invoices'

    def handle(self, *args, **options):
        """
        Process Procurement Orders
        """
        
        Invoice.objects.all().delete()
        # for invoice in invoices:
        #     print u'%s deleted' % invoice
        #     invoice.delete()
            
            
        packings = Packing.objects.all()
        process_packings(packings)
        
        # invoices = Invoice.objects.all()
        # create_invoices(invoices)
        