from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(
        r'^clear_and_gen_procurements/$',
        'shops.views.shops_support_commands',
        name='shop_commands',
    ),
)
