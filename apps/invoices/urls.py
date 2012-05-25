from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("invoices.views",
    url(r"^list/",
        'invoice_list',
        name='invoice-list'),
    #url(r"^invoice/(?P<order_number>[-\d]+)/$",
    url (r"^detail/(?P<slug>[-\d]+)/$",
    	'invoice_detail',
        name='invoice-detail'),
    url(
        r'^create/$',
        'create_invoices',
        name='create_invoices',
    ),      
)