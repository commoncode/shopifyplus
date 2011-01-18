from django.db import models

import shopipy

class Shop(models.Model):
    """
    A Shopify Shop
    """
    
    title = models.CharField(
        max_length=255)
    
    shopify_id = models.IntegerField(
        blank=True,
        null=True)
    
    api_key = models.CharField(
        blank=True, 
        max_length=255)
    host_name = models.CharField(
        max_length=255)
    password = models.CharField(
        blank=True,
        max_length=255)
    
    def __unicode__(self):
        return u"%s" % self.title
        
    def connect(self):
        self.instance = shopipy.Shopify(self.host_name, self.api_key, self.password)
