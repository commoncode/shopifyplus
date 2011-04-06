from django.db import models
from shopifyable.models import Order, OrderItem

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