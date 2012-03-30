from django.db import models
from django.contrib.auth.models import User

from ordering.models import Order, OrderItem
from procurement.models import ProcurementItem
from products.models import ProductVariant


import datetime


class Packing(models.Model):
    """
    Based on Orders & ProcurementItem
    """
    order = models.ForeignKey(Order, unique=True)    

    @property
    def packing_order_cost(self):
        packing_items = PackingItem.objects.filter(packing=self)
        cost = 0
        for packing_item in packing_items:
            cost = cost + packing_item.packing_item_cost
        return cost

    def __unicode__(self):
        return u'%s' % self.order
    
class PackingItem(models.Model):
    """
    Corresponding to OrderItem
    and Procurement Item
    
    Packing values are calculated
    first from procurement items.
    
    Fulfilment values are defaulted
    to the packing values, yet are editable
    for adjustments.
    """
    
    packing = models.ForeignKey(
        Packing,
        editable=False)
    order_item = models.ForeignKey(
        OrderItem,
        editable=False)
    procurement_item = models.ForeignKey(
        ProcurementItem,
        editable=False)
    
    substitue_product_variant = models.ForeignKey(
        ProductVariant,
        blank=True,
        null=True)
    
    packing_weight = models.IntegerField(
        "p'weight",
        editable=False,
        blank=True,
        null=True)
    packing_quantity = models.IntegerField(
        "p'quantity",
        editable=False,
        blank=True,
        null=True)
    packing_unit_weight = models.IntegerField(
        "p'unit weight",
        editable=False,
        blank=True,
        null=True)
    packing_weight_price = models.FloatField(
        "p'weight price",
        editable=False,
        blank=True,
        null=True)
    packing_unit_price = models.FloatField(
        "p'unit price",
        editable=False,
        blank=True,
        null=True)
        
    fulfilment_weight = models.IntegerField(
        "f'weight",
        blank=True,
        null=True)
    fulfilment_quantity = models.IntegerField(
        "f'quantity",
        blank=True,
        null=True)
    fulfilment_unit_weight = models.IntegerField(
        "f'unit weight",
        blank=True,
        null=True)
    fulfilment_weight_price = models.FloatField(
        "f'weight price",
        blank=True,
        null=True)
    fulfilment_unit_price = models.FloatField(
        "f'unit price",
        blank=True,
        null=True)
        
    fulfilled = models.BooleanField()
    fulfilled_by = models.ForeignKey(
        User,
        blank=True,
        null=True)
    fulfilled_at = models.DateTimeField(
        blank=True,
        null=True)
    
    notes = models.TextField(
        blank=True,
        null=True)
        
    class Meta:
        unique_together = (
            'packing',
            'order_item',
            'procurement_item', )
        ordering = (
            'order_item__sku',)
        
    def __unicode__(self):
        return u'%s' % (self.order_item)

    @property
    def packing_item_cost(self):
        return self.packing_unit_price * self.packing_quantity
        
    # def save(self):
    #     """ 
    #     Raise an Integrity Error or like if
    #     the order_item chosen does not belong
    #     to the Order related to via the PackingOrder
    #     """
    #     super.