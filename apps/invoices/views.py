from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect

from shops.models import Shop
from invoices.models import Invoice, InvoiceItem
from fulfilment.models import Packing
from invoices.utils import process_packings, create_invoices

class InvoiceMixin(object):
    model = Invoice
    def get_queryset(self):
        return super(InvoiceMixin, self).get_queryset().select_related().filter()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get()

class InvoiceDetailMixin(object):
    model = Invoice
    def get_queryset(self):
        return super(InvoiceDetailMixin, self).get_queryset().select_related().filter(invoice=invoice)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get()
        
        

class InvoiceList(InvoiceMixin, generic.ListView):
    template_name = "invoices/invoice_list.html"
invoice_list = InvoiceList.as_view()

#class InvoiceDetail(InvoiceDetailMixin, generic.DetailView):
#	pass
#invoice_detail = InvoiceDetail.as_view()

class InvoiceDetailView(generic.DetailView):

	model = Invoice
	slug_field = "id"

	def render(self, context):
		context['invoice'] = object

invoice_detail = InvoiceDetailView.as_view()

def create_invoices(request):
    """
    Generates packing from procurements
    """

    shop = Shop.objects.get()
    
    # TODO: Select from shop only
    packings = Packing.objects.all()

    process_packings(packings)


    return HttpResponseRedirect('/')
