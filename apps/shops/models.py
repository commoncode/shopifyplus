import os

from django.db import models
from django.contrib.contenttypes.models import ContentType
from shopifyable.models import Shop

from django.core.exceptions import ValidationError

class Shop(Shop):
    """
    A  Shop/Store
    """
    
    invoices_blurb = models.TextField(
        blank=True,
        help_text="A note that appears on all invoices")

    @property
    def logo(self):
        try:
            return self.shoplogo_set.all()[0]
        except IndexError:
            return None

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