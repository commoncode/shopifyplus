from django.contrib import admin
from django.db.models import get_model

from ordering.models import OrderLineItem
from aggregates.models import Aggregate, AggregateOrder, AggregateLineItem
from products.models import ProductVariant

def aggregate_orders(modeladmin, request, queryset):
    
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
        else:
            aggregate_order.save()
            
            """
            If successful, add the Order's OrderLineItems, aggregated,
            to the AggregateLineItem's
            """
        
    # Find the distinct product_variants    
     
    order_line_item_kwargs = {
        'order__in': queryset, }
    order_line_items = OrderLineItem.objects.filter(**order_line_item_kwargs) 
            
    product_variant_kwargs = {
        'shopify_product_variant_id__in': order_line_items.values_list('shopify_product_variant_id', flat=True).distinct()}
            
    product_variants = ProductVariant.objects.filter(**product_variant_kwargs).distinct()
            
    
    
    # for order_line_item in order_line_items:
    #     
    #     aggregate_line_item_kwargs = {
    #         'product_variant': order.product_variant,
    #         'order_weight':
    #         'order_quantity':
    #         'order_units':
    #         'order_unit_weight': ,}
    #     aggregate_line_item = AggregateLineItem()
    
    
    
aggregate_orders.short_description = "Aggregate selected orders"

class OrderLineItemAdmin(admin.StackedInline):
    model = get_model('ordering', 'orderlineitem')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderLineItemAdmin, ]
        
    actions = [aggregate_orders]

admin.site.register(get_model('ordering', 'order'), OrderAdmin)