from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(
        r'^procurement/procurement_(?P<procurement_id>\d+).csv$',
        'procurement.views.procurement_csv',
        name="procurement_csv"
    ),
    url(
        r'^create/$',
        'procurement.views.create_procurement_orders',
        name='create_procurement_orders',
    ),
)