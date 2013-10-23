from django.views import generic
from django.core import management
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect

from shops.models import Shop
from invoices.models import Invoice, InvoiceItem
from fulfilment.models import Packing, PackingItem
from procurement.models import Procurement

from fulfilment.utils import packing_item_defaults, process_procurement_orders


class PackingMixin(object):
    model = Packing
    paginate_by = 50

    def get_queryset(self):
        return super(PackingMixin, self).get_queryset().select_related().filter()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get()


class PackingList(PackingMixin, generic.ListView):
    pass
packing_list = PackingList.as_view()


class ShippingList(PackingMixin, generic.ListView):
    template_name = "fulfilment/shipping_list.html"
shipping_list = ShippingList.as_view()


# class PackingDetail(PackingMixin, generic.DetailView):
#     pass
# packing_detail = PackingDetail.as_view()

class PackingDetailView(generic.DetailView):

    model = Packing

    def render(self, context):
        context['packing'] = object

packing_detail = PackingDetailView.as_view()



def create_packing_orders(request):
    """
    Generates packing from procurements
    """

    shop = Shop.objects.get()

    # Delete previous packing/invoices
    # TODO: Keep them! But make sure they get closed
    management.call_command('reset', 'fulfilment', noinput=True, verbosity=0, interactive=False);
    management.call_command('reset', 'invoices', noinput=True, verbosity=0, interactive=False);

    # Create packing
    # TODO: Select the shop only
    print "Creating packing..."
    procurements = Procurement.objects.all()
    packings = process_procurement_orders(procurements)

    # Set packing item defaults
    print "Setting item defaults..."
    items = PackingItem.objects.filter(packing__in=packings)
    packing_item_defaults(items)

    return HttpResponseRedirect('/')
