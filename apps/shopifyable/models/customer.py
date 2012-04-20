"""
HTTP/1.1 200 OK[]
{
  "customers": [
    {
      "accepts_marketing": false,
      "created_at": "2012-03-02T13:52:49-05:00",
      "email": "bob.norman@hostmail.com",
      "first_name": "Bob",
      "id": 207119551,
      "last_name": "Norman",
      "note": null,
      "orders_count": 0,
      "state": null,
      "total_spent": "0.00",
      "updated_at": "2012-03-02T13:52:49-05:00",
      "tags": "",
      "addresses": [
        {
          "address1": "Chestnut Street 92",
          "address2": "",
          "city": "Louisville",
          "company": null,
          "country": "US",
          "first_name": null,
          "id": 207119551,
          "last_name": null,
          "phone": "555-625-1199",
          "province": "KY",
          "zip": "40202",
          "name": null,
          "province_code": null,
          "country_code": null,
          "default": true
        }
      ]
    }
  ]
}
"""

from django.db import models

from shopifyable.models import Shopifyable, Handleable, Taggable
import urllib

class Customer(Shopifyable, Taggable):

    shopify_customer_id = models.PositiveIntegerField(
        blank=True,
        null=True)

    accepts_marketing = models.BooleanField()

    email = models.EmailField(
        blank=True,
        null=True)

    first_name = models.CharField(
        blank=True,
        max_length=1024)

    last_name = models.CharField(
        blank=True,
        max_length=1024)

    note = models.TextField(
        blank=True,
        null=True)

    orders_count = models.PositiveIntegerField(
        blank=True,
        null=True)

    state = models.CharField(
        blank=True,
        max_length=50)

    total_spent = models.FloatField(
        blank=True,
        null=True)

    class Meta:
        abstract = True

    class Shopify:
        shopify_fields = {
            "accepts_marketing": "accepts_marketing",
            "email": "email",
            "first_name": "first_name",
            "id": "id", #"shopify_customer_id",  #TODO: Determine if this works
            "last_name": "last_name",
            "note": "note",
            "orders_count": "orders_count",
            "state": "state",
            "total_spent": "total_spent",
        }
        
        shopify_date_fields = {
            'created_at': 'created_at',
            'updated_at': 'updated_at', }

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
