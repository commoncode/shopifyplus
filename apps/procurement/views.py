# -*- coding: utf-8 -*-
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from invoices.models import Invoice, InvoiceItem
from fulfilment.models import Packing, PackingItem
from procurement.models import Procurement, ProcurementItem, ProcurementOrder
from procurement.utils import procurement_orders
from ordering.models import Order
from shops.models import Shop

from procurement.utils import procurement_item_defaults

def procurement_csv(request, procurement_id):
    
    
    procurement = get_object_or_404(Procurement, id=procurement_id)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=procurement_%s.csv' % procurement_id

    writer = csv.writer(response)
    
    writer.writerow([
        'Vendor', 
        'Product', 
        'Variant', 
        'Quantity', 
        'Grams'])
    
    order_by_args = [
        'product_variant__product__vendor', 
        'product_variant', ]
    procurement_items = procurement.procurementitem_set.all().order_by(*order_by_args)

    for procurement_item in procurement_items: 
        writer.writerow([
            procurement_item.product_variant.product.vendor,
            str(procurement_item.product_variant.product),
            str(procurement_item.product_variant.option1),
            str((procurement_item.order_units) or ''),
            str((procurement_item.order_weight) or '')])
            
    return response

def create_procurement_orders(request):
    """
    Generates procurements from open orders
    """

    shop = Shop.objects.get()

    # Delete previous procurement/packing/invoices
    # TODO: Keep them! But make sure they get closed
    invoices = Invoice.objects.filter(packing__order__shop=shop)
    InvoiceItem.objects.filter(invoice__in=invoices).delete()
    invoices.delete()

    packing = Packing.objects.filter(order__shop=shop)
    proc_order = ProcurementOrder.objects.filter(order__shop=shop)
    packing.delete()
    proc_order.delete()

    # TODO: Delete these for the current shop ONLY.
    ProcurementItem.objects.all().delete()
    Procurement.objects.all().delete()

    orders = Order.objects.filter(opened=True, shop=shop)
    procurement_items = procurement_orders(orders)

    # Set procurement defaults
    print "Setting item defaults"
    procurement_item_defaults(procurement_items)

    return HttpResponseRedirect('/')