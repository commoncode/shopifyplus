from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(
        r'^sync/$',
        'products.views.product_sync_command',
        name='sync_products',
    ),
)
