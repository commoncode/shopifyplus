from django.core.exceptions import ValidationError, ObjectDoesNotExist

from ordering.models import OrderLineItem, Order
from aggregates.models import Aggregate, AggregateOrder, AggregateLineItem
from products.models import ProductVariant


from django.db.models import Sum


def aggregate_orders(queryset):
    
    import ipdb; ipdb.set_trace()
    
    """
    Create a new Aggregate
    """
    aggregate = Aggregate()
    aggregate.save()

    """
    First, loop through the queryset and save the Orders
    to the AggregateOrder model.
    """
    for order in queryset:
        aggregate_order = AggregateOrder(aggregate=aggregate, order=order)
        try:
            aggregate_order.full_clean()
        except ValidationError, e:
            print e
            """
            Validation error is likely to be an Integrity Error
            due to the unique_together constraint on Aggregate and Order
            
            TODO: assemble an error msg, and skip over the order.
            """
        else:
            aggregate_order.save()
            
    # Retrieve the OrderLineItems for later use
    order_line_item_kwargs = {
        'order__in': queryset, }
    order_line_items = OrderLineItem.objects.filter(**order_line_item_kwargs) 
    
    # Get the distinct set of product_variants found in order_line_items
    product_variant_kwargs = {
        'shopify_product_variant_id__in': order_line_items.values_list('shopify_product_variant_id', flat=True).distinct()}
    product_variants = ProductVariant.objects.filter(**product_variant_kwargs).distinct()
    
    for product_variant in product_variants:
        
        oli_kwargs = {
            'shopify_product_variant_id': product_variant.shopify_product_variant_id, }
        
        # Assemble values for kwargs inclusion
        units = order_line_items.filter(**oli_kwargs).aggregate(Sum('quantity'))['quantity__sum']
        grams = product_variant.grams
        order_weight = units * grams
        
        aggregate_line_item_kwargs = {
            'aggregate': aggregate,
            'product_variant': product_variant,
            'order_weight': order_weight,
            'order_units': units, }
        aggregate_line_item = AggregateLineItem(**aggregate_line_item_kwargs)
        
        try:
            aggregate_line_item.full_clean()
        except ValidationError, e:
            print e
        else:
            aggregate_line_item.save()