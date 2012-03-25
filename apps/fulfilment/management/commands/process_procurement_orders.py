from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from fulfilment.utils import process_procurement_orders
from fulfilment.models import Packing, PackingItem
from procurement.models import Procurement

class Command(BaseCommand):
    help = 'process procurement orders'

    def handle(self, *args, **options):
        """
        Process Procurement Orders
        """
        packings = Packing.objects.all()
        for packing in packings:
            packing.delete()

        procurements = Procurement.objects.all()
        process_procurement_orders(procurements)
        