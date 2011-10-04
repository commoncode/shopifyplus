from django.db import models

import datetime, shopifyable, urllib

class Shop(models.Model):
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
        
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return u"%s" % self.title
        
    def connect(self):
        try:
            self._connection
        except AttributeError:
            self._connection = shopifyable.Shopify(self.host_name, self.api_key, self.password)
    
    def shop(self):
        self._shop = self._connection.GET('/admin/shop.json')
        return self._shop
    
    # Products
        
    def products(self, **kwargs):
        """
        limit: 50 to 250 page: 1 vendor product_type collection_id
        created_at_min created_at_max updated_at_min updated_at_max fields:
        comma separated list
        """
        
        # TODO store the _products in a cache or session
        
        kwargs.update({'limit': 250})
        
        self.connect()
        url = '/admin/products.json'
        if kwargs:
            url += '?'+urllib.urlencode(kwargs)
        print url
        self._products_json = self._connection.GET(url)
        
        
        self._products = self._products_json['products']

    def products_count(self, collection=None):
        self.connect()
        url = '/admin/products/count.json'
        if collection:
            url += '?'+urllib.urlencode({'collection_id': collection.id})
        print url
        self._products_count = self._connection.GET(url)
        
    # Orders
    
    def orders(self, **kwargs):
        self.connect()
        url = '/admin/orders.json'
        if kwargs:
            url += '?'+urllib.urlencode(kwargs)
        print url
        self._orders_json = self._connection.GET(url)
        self._orders = self._orders_json['orders'] 

    def update(self, model, etree):
        """
        For a given model, update the values
        supplied within the etree.
        """
        
        for element in list(etree):
            try:
                obj = model.objects.get(**lookup_kwargs(model, element))
            except ObjectDoesNotExist:
                obj = model(shop=self, **element_kwargs(model, element))
            else:
                pass
            try:
                obj.full_clean()
            except ValidationError, e:
                print e
            else:
                obj.save()
                print obj
         
