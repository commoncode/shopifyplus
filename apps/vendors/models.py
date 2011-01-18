from django.db import models

from shops.models import Shop

class Vendor(models.Model):
    """
    A Shopify product vendor
    """
    title = models.CharField(max_length=200)
    
    def __unicode__(self):
        return u'%s' % self.title