from django.db import models

from shopifyable.models import Customer

from shops.models import Shop


class Customer(Customer):
    """
    A Shopify Customer
    """
    shop = models.ForeignKey(
        Shop,
        blank=True,
        null=True)
        
    order = models.ForeignKey(
        'ordering.Order',
        blank=True,
        null=True)
        
    class Meta:
        ordering = ['last_name',]