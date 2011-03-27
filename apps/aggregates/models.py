from django.db import models

from ordering.models import Order
from products.models import ProductVariant

class Aggregate(models.Model):
    """
    Aggregates are created from a set of Orders that 
    are unique together with an Aggregate.
    
    Once the AggregateOrder relationship is created,
    AggregateLineItems are then assembled through
    the Order, OrderLineItem & ProductVariant
    relationships
    """

    # def __unicode__(self):
    #     return u'%s' % self.aggregateorder_set.all()

class AggregateOrder(models.Model):
    """
    An intermediary table between an 
    Aggregate and an Order.
    """
    aggregate = models.ForeignKey(Aggregate)
    order = models.ForeignKey(Order)
    
    class Meta:
        """
        Orders may only be added to a single Aggregate
        at any one time, so they should be unique_together
        """
        unique_together = ('aggregate', 'order')
        
    def __unicode__(self):
        return u'#%s :: #%s' % (self.aggregate, self.order)
    
class AggregateLineItem(models.Model):
    """
    For each product an Aggregated line item is created.
    """
    
    aggregate = models.ForeignKey(Aggregate)
    
    product_variant = models.ForeignKey(ProductVariant)
    
    order_weight = models.IntegerField(
        blank=True,
        null=True)
    order_quantity = models.IntegerField(
        blank=True,
        null=True)
    order_units = models.IntegerField(
        blank=True,
        null=True)
    order_unit_weight = models.FloatField(
        blank=True,
        null=True)
        
    def __unicode__(self):
        return u'%s :: %s units :: %s grams' % (self.product_variant, self.order_units, self.order_weight)