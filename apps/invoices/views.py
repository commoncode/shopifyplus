from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect

from invoices.models import Invoice, InvoiceItem

class InvoiceMixin(object):
    model = Invoice
    def get_queryset(self):
        return super(InvoiceMixin, self).get_queryset().select_related().filter()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get()
        
class InvoiceList(InvoiceMixin, generic.ListView):
    template_name = "invoices/invoice_list.html"
invoice_list = InvoiceList.as_view()

class InvoiceDetail(InvoiceMixin, generic.ListView):
    pass
invoice_detail = InvoiceDetail.as_view()
