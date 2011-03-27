from django.db import models
from shopifyable.models import Order, OrderLineItem

from shops.models import Shop

class Order(Order):
    """
    An Shopify/Food Cart order.
    """
    
    shop = models.ForeignKey(
        Shop)
    
class OrderLineItem(OrderLineItem):
    """
    An Order Line Item
    """
    order = models.ForeignKey(
        Order)