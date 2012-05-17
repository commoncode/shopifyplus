from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from filebrowser.sites import site

urlpatterns = patterns("",
    url(r"^", include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
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
<<<<<<< HEAD
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),

    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += patterns('django.views.static',
        url(r'^media/(?P<path>.*)$',
            'serve',
            { 'document_root': settings.MEDIA_ROOT, },
        ),
    ) + staticfiles_urlpatterns()
>>>>>>> 2e4b2ecfcd6ed3e5f6330dc02251495a0df401bb
