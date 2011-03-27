from django.db import models
from taggit.models import Tag
import datetime    
        
class Shopifyable(models.Model):
    """
    Base abstract Shopify Model.  Based on BaseShopifyElement.
    """
    
    created_at = models.DateTimeField()
    
    pushed_at = models.DateTimeField(
        blank=True,
        null=True)
        
    updated_at = models.DateTimeField(
        blank=True,
        null=True)
     
    synced_at = models.DateTimeField(
        blank=True,
        null=True)
     
    fetched_at = models.DateTimeField(
        blank=True,
        null=True)
        
    class Meta:
        abstract = True

    def fetch(self):
        """
        Fetch corresponding object from Shopify API, overriding/updating
        the data kept locally.
        """
        pass

    def push(self):
        """
        Push to the corresponding object in the Shopify API, overriding
        the data kept remotely.
        """
        pass
    
    def sync(self):
        """
        Check the remote Shopify object for updated-at,
        comparing with the local object and update
        accordingly
        """
        pass
        
class Handleable(models.Model):
    
    handle = models.SlugField(
        max_length=255)
        
    class Meta:
        abstract = True
        
class Taggable(models.Model):
        
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        null=True)
        
    class Meta:
        abstract = True
