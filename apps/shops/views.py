import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import management
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from ordering.models import Order
from procurement.models import Procurement
from products.models import Product
from shops.models import Shop

from .tasks import shops_support_commands_task

@login_required
def shops_support_commands(request):
    """
    Chains together managment commands
    for procurement work flow

    python manage.py reset products --noinput
    python manage.py get_products
    python manage.py reset ordering --noinput
    python manage.py get_orders
    python manage.py create_procurement_items
    """

    messages.add_message(request, messages.INFO, 'Starting Procurements.  An SMS will be sent to 0402 231 007 when complete.')

    shops_support_commands_task.delay()

    return HttpResponseRedirect('/')

def shops_procurement_email_csv(request):
    """
    A Shortcut View to create procurements for
    all Shops, resetting and fetching Products
    & Orders
    """

    Order.objects.all().delete()
    Product.objects.all().delete()

    procurements = Procurement.objects.all()

    if procurements:
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=procurement_%s.csv' % procurement_id

    for procurement in procurements:

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
