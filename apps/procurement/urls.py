from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(
        r'^procurement/procurement_(?P<procurement_id>\d+).csv$',
        'procurement.views.procurement_csv',
        name="procurement_csv"
    ), )