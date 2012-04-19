from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db.models import Sum

from ordering.models import OrderItem, Order
from procurement.models import Procurement, ProcurementOrder, ProcurementItem
from products.models import ProductVariant


import datetime


def procurement_item_defaults(queryset):
    """
    For each ProcurementItem set the procurement values
    to the aggregated order values
    """
    try:
        if isinstance(queryset[0], Procurement):
            procurement_items = []
            for procurement in queryset:
                 procurement_items += procurement.procurementitem_set.all()
        else:
            procurement_items = queryset
    except IndexError:
        """
        queryset[0] throws IndexError?
        """
        pass
    else:
        for procurement_item in procurement_items:
        
            try:
                procurement_weight_price = float(1000.00) / float(procurement_item.product_variant.grams) * procurement_item.product_variant.price
            except:
                procurement_weight_price = None
            
            procurement_item.procurement_weight = procurement_item.order_weight
            procurement_item.procurement_quantity = procurement_item.order_quantity
            procurement_item.procurement_unit_weight = procurement_item.product_variant.grams
            procurement_item.procurement_weight_price = procurement_weight_price
            procurement_item.procurement_unit_price = procurement_item.product_variant.price
            procurement_item.procured = True
            procurement_item.procured_by = User.objects.get(pk=1)
            procurement_item.procured_at = datetime.datetime.now()
            procurement_item.save()
            
        return procurement_items



def procurement_orders(queryset):
    
    """
    Create a new Procurement
    """
    procurement = Procurement()
    procurement.save()

    """
    First, loop through the queryset and save the Orders
    to the ProcurementOrder model.
    """
    for order in queryset:
        procurement_order = ProcurementOrder(procurement=procurement, order=order)
        try:
            procurement_order.full_clean()
        except ValidationError, e:
            print u'*** ERROR %s' % e
            """
            Validation error is likely to be an Integrity Error
            due to the unique_together constraint on Procurement and Order
            
            TODO: assemble an error msg, and skip over the order.
            """
        else:
            procurement_order.save()
            print "Saved procurement order"
            
    # Retrieve the OrderItems for later use
    order_item_kwargs = {
        'order__in': queryset, }
    order_items = OrderItem.objects.filter(**order_item_kwargs) 
    
    # Get the distinct set of product_variants found in order_items
    product_variant_kwargs = {
        'shopify_product_variant_id__in': order_items.values_list('shopify_product_variant_id', flat=True).distinct()}
    product_variants = ProductVariant.objects.filter(**product_variant_kwargs).distinct()
    
    for product_variant in product_variants:
        
        oli_kwargs = {
            'shopify_product_variant_id': product_variant.shopify_product_variant_id, }
        
        # Assemble values for kwargs inclusion
        units = order_items.filter(**oli_kwargs).aggregate(Sum('quantity'))['quantity__sum']
        grams = product_variant.grams
        order_weight = units * grams
        
        procurement_item_kwargs = {
            'procurement': procurement,
            'product_variant': product_variant,
            'order_weight': order_weight,
            'order_units': units, }
        procurement_item = ProcurementItem(**procurement_item_kwargs)
        
        try:
            procurement_item.full_clean()
        except ValidationError, e:
            print u'*** ERROR %s' % e
        else:
            procurement_item.save()
            print "Saved procurement item"