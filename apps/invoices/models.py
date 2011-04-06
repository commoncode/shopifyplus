from django.db import models
from django.contrib.auth.models import User

from fulfilment.models import Packing, PackingItem

import datetime

class Invoice(models.Model):
    
    # order, customer thru packing ?
    packing = models.ForeignKey(
        Packing,
        unique=True)
    
    signed_off = models.BooleanField()
    signed_off_by = models.ForeignKey(
        User,
        blank=True,
        null=True)
    signed_off_key = models.CharField(
        blank=True,
        help_text="Confirm sign off by entering your user password",
        max_length=255,
        null=True)
    signed_off_at = models.DateTimeField(
        blank=True,
        default=datetime.datetime.now(),
        null=True)
    
    """
    Signing off an invoice will convert all
    InvoiceItems to done=True
    """
    
class InvoiceItem(models.Model):
    
    invoice = models.ForeignKey(Invoice)
    packing_item = models.ForeignKey(PackingItem)
    
    invoice_weight = models.IntegerField(
        "i'weight",
        blank=True,
        null=True)
    invoice_quantity = models.IntegerField(
        "i'quantity",
        blank=True,
        null=True)
    invoice_unit_weight = models.IntegerField(
        "i'unit weight",
        blank=True,
        null=True)
    invoice_weight_price = models.FloatField(
        "i'weight price",
        blank=True,
        null=True)
    invoice_unit_price = models.FloatField(
        "i'unit price",
        blank=True,
        null=True)
        
    notes = models.TextField(
        blank=True,
        null=True)
        
    done = models.BooleanField()
        
    """
    If the invoice is signed_off, changes should
    not be allowed to the InvoiceItems
    """
    