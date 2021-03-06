"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'shopifyplus.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Shopify Plus'),
            column=1,
            collapsible=True,
            children = [
                modules.AppList(
                    _('Shopify Plus'),
                    column=1,
                    collapsible=True,
                    models=(
                        'customers.*',
                        'fulfilment.*',
                        'invoices.*',
                        'ordering.models.Order',
                        'procurement.*',
                        'products.*',
                        'shops.*', ),
                ),
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('AppList: Applications'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('ModelList: Administration'),
            column=1,
            collapsible=False,
            models=('django.contrib.*',),
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Fulfilments'),
            column=2,
            children=[
                {
                    'title': _('Fulfilment Packings List'),
                    'url': '/fulfilment/packings/',
                    'external': False,
                },
            ]
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Procurement Work Flow'),
            column=2,
            children=[
                {
                    'title': _('1. Sync Products'),
                    'url': '/products/sync',
                    'external': False,
                },
                {
                    'title': _('2. Get Open Orders'),
                    'url': '/ordering/sync',
                    'external': False,
                },
                {
                    'title': _('3. Create Procurement Orders (defaults)'),
                    'url': '/procurement/create',
                    'external': False,
                },
                {
                    'title': _('4. Create Packing Orders (defaults)'),
                    'url': '/fulfilment/create',
                    'external': False,
                },
                {
                    'title': _('5. Create Invoices'),
                    'url': '/invoices/create',
                    'external': False,
                },
                # {
                #     'title': _('4. Download Procurement CSV'),
                #     'url': '/procurement/csv?defaults=true',
                #     'external': False,
                # },
                {
                    'title': _('6. Clear & Generate Procurements'),
                    'url': '/shops/clear_and_gen_procurements/',
                    'external': False,
                },
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


