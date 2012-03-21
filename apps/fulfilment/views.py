from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect

from fulfilment.models import Packing, PackingItem

class PackingMixin(object):
    model = Packing
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


class PackingDetail(PackingMixin, generic.DetailView):
    pass
packing_detail = PackingDetail.as_view()