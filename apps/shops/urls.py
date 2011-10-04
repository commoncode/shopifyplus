from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(
        r'^procurements/csv/$',
        'shops.views.shops_procurement_csv',
        name="shops_procurement_csv"
    ), )