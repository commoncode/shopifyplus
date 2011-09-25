from django.db import models
from shopifyable.models import BillingAddress, Order, OrderItem, ShippingLine, ShippingAddress

from shops.models import Shop

class Order(Order):
    """
    An Shopify/Food Cart order.
    """
    shop = models.ForeignKey(
        Shop)
    
class OrderItem(OrderItem):
    """
    An Order Item
    """
    order = models.ForeignKey(
        Order)
        
class BillingAddress(BillingAddress):
    
    order = models.ForeignKey(
        Order)
        
class ShippingAddress(ShippingAddress):
    
    order = models.ForeignKey(
        Order)
        
class ShippingLine(ShippingLine):
    
    order = models.ForeignKey(
        Order)    