from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("fulfilment.views",
    url(r"^packings/$",
        'packing_list',
        name='packing-list'),

    url (r"^packings/(?P<pk>[-\d]+)/$",
        'packing_detail',
        name='packing-detail'),   
    
    # Shipping    
    url(r"^shippings/$",
        'shipping_list',
        name='shipping-list'),
    url(
        r'^create/$',
        'create_packing_orders',
        name='create_packing_orders',
    ),    
)