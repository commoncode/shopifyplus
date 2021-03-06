from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from fulfilment.models import Packing, PackingItem

from django.utils import timezone

class Invoice(models.Model):

    # order, customer thru packing ?
    packing = models.ForeignKey(
        Packing,
        editable=False,
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
        default=timezone.now(),
        null=True)

    notes = models.TextField(
        blank=True)

    def __unicode__(self):
        return u'%s' % self.packing

    @property
    def logo(self):
        return self.packing.order.shop.logo.image.url

    @property
    def taxlines(self):
        '''Generate the taxlines as a list of prices'''
        return self.packing.order.taxline_set.all().values_list('price', flat=True)

    @property
    def shipplinglines(self):
        return self.packing.order.shippingline_set.all().values_list('price', flat=True)

    @property
    def total_discounts(self):
        return self.packing.order.total_discounts

    @property
    def subtotal_price(self):
        return sum([
            (invoice_item.invoice_quantity * invoice_item.invoice_unit_price) for invoice_item in self.invoiceitem_set.all()
        ])

    def total_price(self):
        return sum([self.subtotal_price, -(self.total_discounts), ] + list(self.taxlines) + list(self.shipplinglines))

class InvoiceItem(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        editable=False)

    packing_item = models.ForeignKey(
        PackingItem,
        editable=False)

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

    @property
    def invoice_item_cost(self):
        return self.invoice_unit_price * self.invoice_quantity

    def __unicode__(self):
        return u'%s :: %s' % (self.invoice, self.packing_item)

    """
    If the invoice is signed_off, changes should
    not be allowed to the InvoiceItems
    """