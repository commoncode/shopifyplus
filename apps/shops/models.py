import os

from django.db import models
from django.contrib.contenttypes.models import ContentType
from shopifyable.models import Shop

from django.core.exceptions import ValidationError

class Shop(Shop):
    """
    A  Shop/Store
    """
    pass

class ShopLogo(models.Model):
    """
    A logo for a shop (used for invoices)
    """
    def get_upload_path(instance, filename):
        return os.path.join(
            "shoplogos/%s_%d/" % (instance.shop.title, instance.shop.id), filename)

    shop = models.ForeignKey(
            Shop,
            blank=True,
            null=True,
            unique=True)

    image = models.ImageField(upload_to=get_upload_path)

    def __unicode__(self):
        return u'%s' % self.shop