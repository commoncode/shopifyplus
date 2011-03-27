from django.db import models
from shopifyable.models import Shop

from django.core.exceptions import ValidationError

class Shop(Shop):
    """
    A Shopify Shop/Store
    """
    