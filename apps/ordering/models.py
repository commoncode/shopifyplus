from django.db import models
from shopifyable.models import BillingAddress, Order, OrderItem, ShippingLine, \
    ShippingAddress, DiscountCode
from shopifyable.models.order import TaxLine

from shops.models import Shop

class Order(Order):
    """
    An Shopify/Food Cart order.
    """
    shop = models.ForeignKey(
        Shop)

    opened = models.BooleanField(default=True)

    # customer = models.ForeignKey(
    #     'customers.Customer',
    #     blank=True,
    #     null=True)
    
    @property
    def customer(self):
        try:
            return self.customer_set.all()[0]
        except IndexError:
            return None

    @property
    def shipping_address(self):
        try:
            sa = self.shippingaddress_set.all()[0]
            return '%s, %s' % (
                sa.address1,
                sa.city)
        except IndexError:
            return ''

    @property
    def billing_address(self):
        try:
            sa = self.billingaddress_set.all()[0]
            return '%s, %s' % (
                sa.address1,
                sa.city)
        except IndexError:
            return ''
    
    class Meta:
        ordering = ['-opened',]


class OrderItem(OrderItem):
    """
    An Order Item
    """
    order = models.ForeignKey(
        Order)
    
    @property
    def variant_short_title(self):
        return self.variant_title.split('/')[0]
    
    @property
    def short_name(self):
        return self.name.split('/')[0]
    

class BillingAddress(BillingAddress):

    order = models.ForeignKey(
        Order)

class ShippingAddress(ShippingAddress):

    order = models.ForeignKey(
        Order)

class ShippingLine(ShippingLine):

    order = models.ForeignKey(
        Order)
        
class DiscountCode(DiscountCode):

    order = models.ForeignKey(
        Order)    

class TaxLine(TaxLine):

    order = models.ForeignKey(
        Order)