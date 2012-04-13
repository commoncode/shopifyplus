from django.db import models

from shopifyable.models import Shopifyable, Handleable, Taggable
import urllib

class ProductVariant(Shopifyable):
    
    shopify_product_variant_id = models.PositiveIntegerField(
        blank=True,
        null=True)
        
    shopify_product_id = models.PositiveIntegerField(
        blank=True,
        null=True)
        
    sku = models.CharField(
        blank=True,
        max_length=255,
        null=True)

    title = models.CharField(
        blank=True,
        max_length=1024,
        null=True)

    position = models.IntegerField(
        blank=True,
        null=True)

    option1 = models.CharField(
        blank=True,
        max_length=1024,
        null=True)
    option2 = models.CharField(
        blank=True,
        max_length=1024,
        null=True)
    option3 = models.CharField(
        blank=True,
        max_length=1024,
        null=True)
        
    grams = models.PositiveIntegerField(
        blank=True,
        null=True)

    requires_shipping = models.BooleanField()
    fulfillment_service = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    inventory_management = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    inventory_policy = models.TextField(
        blank=True,
        null=True)
    inventory_quantity = models.IntegerField(
        blank=True,
        null=True)
    price = models.FloatField(
        blank=True,
        null=True)
    compare_at_price = models.FloatField(
        blank=True,
        null=True)
    taxable = models.BooleanField()
    
    class Meta:
        abstract = True
        
    class Shopify:
        shopify_fields = {
            "compare_at_price": "compare_at_price",
            "fulfillment_service": "fulfillment_service",
            "grams": "grams",
            "id": "shopify_product_variant_id",
            "inventory_management": "inventory_management",
            "inventory_policy": "inventory_policy",
            "inventory_quantity": "inventory_quantity",
            "option1": "option1",
            "option2": "option2",
            "option3": "option3", 
            "position": "position",
            "price": "price",
            "requires_shipping": "requires_shipping",
            "sku": "sku",
            "taxable": "taxable",
            "title": "title", }
        # shopify_date_fields = {
        #     'created_at': 'created_at',
        #     'updated_at': 'updated_at', }
        
    def __unicode__(self):
        return u'%s' % self.option1

class Product(Shopifyable, Handleable, Taggable):
    """
    An abstract model that Interfaces with its
    Shopify counterpart.
    """ 
    
    shopify_product_id = models.PositiveIntegerField(
        blank=True,
        null=True)
    
    title = models.CharField(
        blank=True,
        max_length=1024,
        null=True)
        
    body_html = models.TextField(
        blank=True,
        null=True)
        
    published_at = models.DateTimeField(
        blank=True,
        null=True)
        
    template_suffix = models.CharField(
        blank=True,
        max_length=255,
        null=True)
        
    product_type = models.CharField(
        blank=True,
        max_length=255,
        null=True)
        
    vendor = models.CharField(
        blank=True,
        max_length=255,
        null=True)
        
    class Meta:
        abstract = True
        
    class Shopify:
        shopify_fields = {
            'body_html': 'body_html',
            'handle': 'handle',
            'id': 'shopify_product_id',
            'product_type': 'product_type',
            'template_suffix': 'template_suffix',
            'title': 'title',
            'vendor': 'vendor',
            # 'tags': 'tags',
            # 'variants': 'variants',
            # 'images': 'images',
            # 'options': 'options', 
            }
        shopify_arrays = {
            'variants': 'products.ProductVariant', }
        shopify_date_fields = {
            'created_at': 'created_at',
            'published_at': 'published_at',
            'updated_at': 'updated_at' }
        
    def __unicode__(self):
        return u'%s' % self.title
        
    def variants(self, **kwargs):
        """
        limit: 50 to 250 page: 1 vendor product_type collection_id
        created_at_min created_at_max updated_at_min updated_at_max fields:
        comma separated list
        """
        
        self.shop.connect()
        url = '/admin/products/%s/variants.xml' % self.shopify_product_id
        if kwargs:
            url += '?'+urllib.urlencode(kwargs)
        print url
        self._variants = self.shop._connection.GET(url)
