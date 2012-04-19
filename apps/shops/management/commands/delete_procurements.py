from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from invoices.models import Invoice, InvoiceItem
from fulfilment.models import Packing, PackingItem
from procurement.models import Procurement, ProcurementOrder, ProcurementItem       


class Command(BaseCommand):
    help = 'Remove procurements and all foreign keys'

    def handle(self, *args, **options):
        """
        Delete packings, invoices, procurements and all items
        """
        InvoiceItem.objects.all().delete()
        Invoice.objects.all().delete()

        Packing.objects.all().delete()
        PackingItem.objects.all().delete()

        Procurement.objects.all().delete()
        ProcurementOrder.objects.all().delete()
        ProcurementItem.objects.all().delete()

