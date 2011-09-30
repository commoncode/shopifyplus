from django.db import models

from shopifyable.models import Shopifyable

class OrderItem(models.Model):
            
    shopify_product_id = models.PositiveIntegerField(
        blank=True,
        null=True)
    shopify_product_variant_id = models.PositiveIntegerField(
        blank=True,
        null=True)
        
    """
    Derive shopify_order_id from the parent order.
    """    
    shopify_order_id = models.PositiveIntegerField(
        blank=True,
        null=True)
    shopify_order_item_id = models.PositiveIntegerField(
        blank=True,
        null=True)
    fulfillment_service = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    fulfillment_status = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    grams = models.PositiveIntegerField(
        blank=True,
        null=True)
    name = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    price = models.FloatField(
        blank=True,
        null=True)
    grams = models.PositiveIntegerField(
        blank=True,
        null=True)
    
    quantity = models.PositiveIntegerField()

    requires_shipping = models.BooleanField()
    
    sku = models.CharField(
        blank=True,
        max_length=255,
        null=True)
        
    title = models.CharField(
        blank=True,
        max_length=255,
        null=True)
        
    variant_title = models.CharField(
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
        """
        Shopify field name on the left, and the corresponding
        Django ORM model field (on the right)
        """
        shopify_fields = {
            "fulfillment_service": "fulfillment_service",
            "fulfillment_status": "fulfillment_status",
            "grams": "grams",
            "id": "id",
            "name": "name", 
            "price": "price",
            "product_id": "shopify_product_id",
            "quantity": "quantity",
            "requires_shipping": "requires_shipping",
            "sku": "sku",
            "title": "title",
            "variant_id": "shopify_product_variant_id",
            "variant_title": "variant_title",
            "vendor": "vendor", }
        
    def __unicode__(self):
        return u'%s :: %s' % (self.title, self.variant_title)
        
class ShippingLine(models.Model):
    
    price = models.FloatField()
    code = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    title = models.CharField(
        blank=True,
        max_length=255,
        null=True)
        
    class Meta: 
        abstract = True
        
    class Shopify:
        shopify_fields = {
            "price": "price",
            "code": "code",
            "title": "title", }
        
    def __unicode__(self):
        return u'%s' % (self.title)
        
class OrderAddress(models.Model):

    name = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    first_name = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    last_name = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    address1 = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    address2 = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    city = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    company = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    zip = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    country_code = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    country = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    province = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    province_code = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    latitude = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    longitude = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
    phone = models.CharField(
        blank=True, 
        max_length=255,
        null=True)
        
    class Meta: 
        abstract = True
        
    class Shopify:
        shopify_fields = {
            "name": "name",
            "address1": "address1",
            "city": "city",
            "company": "company",
            "address2": "address2",
            "latitude": "latitude",
            "zip": "zip",
            "country_code": "country_code",
            "country": "country",
            "province_code": "province_code",
            "last_name": "last_name",
            "phone": "phone",
            "longitude": "longitude",
            "province": "province",
            "first_name": "first_name", }
            
    def __unicode__(self):
        return u'%s' % (self.address1)
            
class BillingAddress(OrderAddress):
    
    class Meta:
        abstract = True
        
    class Shopify:
        shopify_fields = OrderAddress.Shopify.shopify_fields
        
class ShippingAddress(OrderAddress):
    
    class Meta:
        abstract = True
        
    class Shopify:
        shopify_fields = OrderAddress.Shopify.shopify_fields

class Order(Shopifyable):
    """
    An abstract model that Interfaces with its
    Shopify counterpart.
    """
    
    shopify_order_id = models.PositiveIntegerField(
        blank=True,
        null=True)
    browser_ip = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    buyer_accepts_marketing = models.BooleanField()
    closed_at = models.DateTimeField(
        blank=True,
        null=True)
    currency = models.CharField(
        blank=True,
        max_length=4,
        null=True)
    customer = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    email = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    financial_status = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    fulfillment_status = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    gateway = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    landing_site = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    landing_site_ref = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    name = models.CharField(
        max_length=10)
    note = models.TextField(
        blank=True,
        null=True)
    note_attributes = models.TextField(
        blank=True,
        null=True)
    number = models.CharField(
        blank=True,
        max_length=10,
        null=True)
    order_number = models.CharField(
        blank=True,
        max_length=10,
        null=True)
    referring_site = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    subtotal_price = models.FloatField(
        blank=True,
        null=True)
    taxes_included = models.BooleanField()
    tax_lines = models.TextField(
        blank=True,
        null=True)
    token = models.CharField(
        blank=True,
        max_length=255,
        null=True)
    total_discounts = models.FloatField(
        blank=True,
        null=True)
    total_line_items_price = models.FloatField(
        blank=True,
        null=True)
    total_price = models.FloatField(
        blank=True,
        null=True)
    total_weight = models.PositiveIntegerField(
        blank=True,
        null=True)
    total_tax = models.FloatField(
        blank=True,
        null=True)
    
    class Meta: 
        abstract = True
        
    class Shopify:
        shopify_fields = {
            'browser_ip': 'browser_ip',
            'buyer_accepts_marketing': 'buyer_accepts_marketing',
            'currency': 'currency',
            'customer': 'customer',
            'email': 'email',
            'financial_status': 'financial_status',
            'fulfillment_status': 'fulfillment_status',
            'gateway': 'gateway',
            'id': 'shopify_order_id',
            'landing_site': 'landing_site',
            'landing_site_ref': 'landing_site_ref',
            'name': 'name',
            'note': 'note',
            'note_attributes': 'note_attributes',
            'number': 'number',
            'order_number': 'order_number',
            'referring_site': 'referring_site',
            'subtotal_price': 'subtotal_price',
            'tax_lines': 'tax_lines',
            'taxes_included': 'taxes_included',
            'token': 'token',
            'total_discounts': 'total_discounts',
            'total_line_items_price': 'total_line_items_price',
            'total_price': 'total_price',
            'total_tax': 'total_tax',
            'total_weight': 'total_weight', }
        shopify_date_fields = {
            'closed_at': 'closed_at',
            'created_at': 'created_at',
            'updated_at': 'updated_at', }
        shopify_arrays = {
            'line_items': 'ordering.OrderItem',
            'shipping_lines': 'ordering.ShippingLine', }
        shopify_dicts = {
            'billing_address': 'ordering.BillingAddress',
            'shipping_address': 'ordering.ShippingAddress', }

    def __unicode__(self):
        return u'%s' % (self.order_number)
        