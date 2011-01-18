from django.db import models

from filebrowser.fields import FileBrowseField
from shops.models import Shop
from taggit.models import Tag


class Product(models.Model):
    """
    Product model to match Shopify
    """
    
    shop = models.ForeignKey(
        Shop)
    
    shopify_product_id = models.PositiveIntegerField()
    
    title = models.CharField(
        max_length=255)
    handle = models.SlugField(
        max_length=255)
    body_html = models.TextField(
        blank=True)
        
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(
        blank=True)
    published_at = models.DateTimeField(
        blank=True)
        
    template_suffix = models.CharField(
        blank=True,
        max_length=255)
    product_type = models.CharField(
        blank=True,
        max_length=255)
    vendor = models.CharField(
        blank=True,
        max_length=255)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        null=True)
    
    def __unicode__(self):
        return u'%s' % self.title
        
    def pull(self):
        """
        Pull from Shopify
        """
        pass
        
    def push(self):
        """
        Push to Shopify
        """
        pass
        
    def is_updated(self):
        """
        Compare 'updated_at' timestamps
        """
        pass
    
    # product = Product().parse_xml(WSP.GET('/admin/products/9486002.xml'))

class ProductVariant(models.Model):
    """
    ProductVariant model to match Shopify
    """
    
    shop = models.ForeignKey(
        Shop)
    product_id = models.ForeignKey(
        Product)
        
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(
        blank=True,
        null=True)

    sku = models.CharField(
        blank=True,
        max_length=255)

    title = models.CharField(
        max_length=255)

    position = models.IntegerField(
        blank=True)

    option1 = models.CharField(
        blank=True,
        max_length=255)
    option2 = models.CharField(
        blank=True,
        max_length=255)
    option3 = models.CharField(
        blank=True,
        max_length=255)
        
    grams = models.PositiveIntegerField(
        blank=True)

    requires_shipping = models.BooleanField()
    fulfillment_service = models.CharField(
        blank=True,
        max_length=255)
    inventory_management = models.CharField(
        blank=True,
        max_length=255)
    inventory_policy = models.TextField(
        blank=True,
        null=True)
    inventory_quantity = models.IntegerField(
        blank=True,
        null=True)
    price = models.FloatField(
        blank=True)
    compare_at_price = models.FloatField(
        blank=True)
    taxable = models.BooleanField()
    
    def __unicode__(self):
        return u'%s' % self.title

class ProductImage(models.Model):
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


    
    