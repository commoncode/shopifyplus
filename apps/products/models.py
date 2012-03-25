from django.db import models

from filebrowser.fields import FileBrowseField
from shopifyable.models import Product, ProductVariant

from shops.models import Shop
from taggit.models import Tag


class Collection(models.Model):
    """
    A Shopify Collection
    """
    handle = models.SlugField(
        max_length=255)
    body_html = models.TextField(
        blank=True)
        
    def __unicode__(self):
        return u'%s' % self.handle
    
class Product(Product):
    """
    A Shopify Product
    """
    
    shop = models.ForeignKey(
        Shop)
        
    class Meta:
        ordering = ['title']

class ProductVariant(ProductVariant):
    """
    A Shopify Product Variant
    """
    
    product = models.ForeignKey(
        Product)
        
    class Meta:
        ordering = ['title']
        


class ProductImage(models.Model):
    """
          "position": 1,
          "created_at": "2011-03-18T16:23:14-04:00",
          "updated_at": "2011-03-18T16:23:14-04:00",
          "src": "http://static.shopify.com/s/files/1/6909/3384/products/ipod-nano.png?30",
          "id": 850703190
    """
    
    shop = models.ForeignKey(
        Shop)
    product = models.ForeignKey(Product)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(
        blank=True,
        null=True)

    position = models.PositiveIntegerField()

    src = FileBrowseField(
        directory="products", 
        max_length=255,
        null=True)
        
    def __unicode__(self):
        return u'%s' % self.src

class ProductOption(models.Model):
    product = models.ForeignKey(
        Product)
    name = models.CharField(
        max_length=255)
        
    def __unicode__(self):
        return u'%s' % self.name


    
    