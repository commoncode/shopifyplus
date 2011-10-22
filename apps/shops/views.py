import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from procurement.models import Procurement
from shops.models import Shop
from ordering.models import Order
from products.models import Product

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