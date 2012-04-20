from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(
        r'^sync/$',
        'ordering.views.ordering_sync_command',
        name='ordering_commands',
    ),
)
