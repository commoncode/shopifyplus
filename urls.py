from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^", include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
)

# ShopifyPlus
urlpatterns += patterns("",
    url(r"^procurement/", include('procurement.urls')),
)

# ShopifyPlus
urlpatterns += patterns("",
    url(r"^shops/", include('shops.urls')),
    url(r"^fulfilment/", include('fulfilment.urls')),
    url(r"^invoices/", include('invoices.urls')),
    url(r"^products/", include('products.urls')),
    url(r"^ordering/", include('ordering.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
