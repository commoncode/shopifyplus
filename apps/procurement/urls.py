from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(
        r'^procurement/(?P<procurement_id>.*)/csv/$',
        'procurement.views.procurement_csv',
        name="procurement_csv"
    ), )