from django.db import models

from shopifyable.models import Shopifyable


class OrderLineItem(models.Model):
            
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
    shopify_order_line_item_id = models.PositiveIntegerField(
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
        shopify_fields = {
            "fulfillment-service": "fulfillment_service",
            "fulfillment-status": "fulfillment_status",
            "grams": "grams",
            "id": "shopify_order_line_item_id",
            "name": "name", 
            "price": "price",
            "product-id": "shopify_product_id",
            "quantity": "quantity",
            "requires-shipping": "requires_shipping",
            "sku": "sku",
            "title": "title",
            "variant-id": "shopify_product_variant_id",
            "variant-title": "variant_title",
            "vendor": "vendor", }

        
    def __unicode__(self):
        return u'%s' % self.title 

class Order(Shopifyable):
    """
    An abstract model that Interfaces with its
    Shopify counterpart.
    """
    
    shopify_order_id = models.PositiveIntegerField(
        blank=True,
        null=True)
    
    billing_address = models.TextField(
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
    # created_at = models.DateTimeField()
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
    # line_items Inline FK
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
    shipping_address = models.TextField(
        blank=True,
        null=True)
    shipping_lines = models.TextField(
        blank=True,
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
    # updated_at = models.DateTimeField(
    #     blank=True,
    #     null=True)
    total_tax = models.FloatField(
        blank=True,
        null=True)
    
    class Meta: 
        abstract = True
        
    class Shopify:
        shopify_fields = {
            'number': 'number',
            'name': 'name',
            'created-at': 'created_at',
            'total-discounts': 'total_discounts',
            'token': 'token',
            'updated-at': 'updated_at',
            'total-price': 'total_price',
            'landing-site': 'landing_site',
            'taxes-included': 'taxes_included',
            'id': 'shopify_order_id',
            'referring-site': 'referring_site',
            'total-line-items-price': 'total_line_items_price',
            'subtotal-price': 'subtotal_price',
            'note': 'note',
            'gateway': 'gateway',
            'fulfillment-status': 'fulfillment_status',
            'financial-status': 'financial_status',
            'currency': 'currency',
            'closed-at': 'closed_at',
            'buyer-accepts-marketing': 'buyer_accepts_marketing',
            'total-tax': 'total_tax',
            'total-weight': 'total_weight',
            'email': 'email',
            'browser-ip': 'browser_ip',
            'landing-site-ref': 'landing_site_ref',
            'order-number': 'order_number',
            'customer': 'customer',
            'tax-lines': 'tax_lines',
            'shipping-address': 'shipping_address',
            'shipping-lines': 'shipping_lines',
            'billing-address': 'billing_address',
            'note-attributes': 'note_attributes',
            'line-items': OrderLineItem }
        shopify_arrays = {
            'line-items': OrderLineItem,
        }

    def __unicode__(self):
        return u'%s' % self.order_number
        