from django.db import models
from django.contrib.auth.models import User
from ordering.models import Order
from products.models import ProductVariant
from django.db.models import Min, Max

from shops.models import Shop

from django.utils import timezone

class Procurement(models.Model):
    """
    Procurements are created from a set of Orders that 
    are unique together with an Procurement.
    
    Once the ProcurementOrder relationship is created,
    ProcurementItems are then assembled through
    the Order, OrderItem & ProductVariant
    relationships
    """
    
    # shops = models.ManyToManyField(
    #     Shop,
    #     help_text="Procurement for shops")
    created_at = models.DateTimeField()
    
    def __unicode__(self):
        return '%s' % self.created_at
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        super(Procurement, self).save(*args, **kwargs)
        
        # shop_kwargs = {
        #     'id__in': self.procurementorder_set.all().values_list('order__shop__id', flat=True), }    
        # self.shops = Shop.objects.filter(**shop_kwargs)
        
    def _order_numbers(self):
        return self.procurementorder_set.all().values_list('order__order_number', flat=True)
        
    def _shops(self):
        return ', '.join(set(self.procurementorder_set.all().values_list('order__shop__title', flat=True)))
    
    @models.permalink
    def get_csv_url(self):
        return (
            'procurement_csv',
            (),
            { 'procurement_id': self.id, })    
    
class ProcurementOrder(models.Model):
    """
    An intermediary table between an 
    Procurement and an Order.
    """
    procurement = models.ForeignKey(Procurement)
    order = models.ForeignKey(Order)
    
    class Meta:
        """
        Orders may only be added to a single Procurement
        at any one time, so they should be unique_together
        """
        unique_together = ('procurement', 'order')
        
    def __unicode__(self):
        return u'#%s :: #%s' % (self.procurement, self.order)
    
class ProcurementItem(models.Model):
    """
    For each product an Procurementd line item is created.
    """
    
    procurement = models.ForeignKey(Procurement)
    
    product_variant = models.ForeignKey(
        ProductVariant,
        editable=False,
        related_name="ordered_product_variant")
        
    substitute_product_variant = models.ForeignKey(
        ProductVariant,
        blank=True,
        related_name="subtitute_product_variant",
        null=True,)
    
    order_weight = models.IntegerField(
        blank=True,
        editable=False,
        null=True)
    order_quantity = models.IntegerField(
        blank=True,
        editable=False,
        null=True)
    order_units = models.IntegerField(
        blank=True,
        editable=False,
        null=True)
    order_unit_weight = models.IntegerField(
        blank=True,
        editable=False,
        null=True)
        
    procurement_weight = models.IntegerField(
        "p'weight",
        blank=True,
        null=True)
    procurement_quantity = models.IntegerField(
        "p'quantity",
        blank=True,
        null=True)
    procurement_unit_weight = models.IntegerField(
        "p'unit weight",
        blank=True,
        null=True)
    procurement_weight_price = models.FloatField(
        "p'weight price",
        blank=True,
        null=True)
    procurement_unit_price = models.FloatField(
        "p'unit price",
        blank=True,
        null=True)
        
    procured = models.BooleanField()
    procured_by = models.ForeignKey(
        User,
        blank=True,
        null=True)
    procured_at = models.DateTimeField(
        blank=True,
        null=True)
        
    def __unicode__(self):
        return u'%s :: %s units :: %s grams' % (self.product_variant, self.order_units, self.order_weight)