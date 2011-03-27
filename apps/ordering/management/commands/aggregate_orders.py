from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from ordering.models import OrderLineItem, Order
from aggregates.models import Aggregate, AggregateOrder, AggregateLineItem
from products.models import ProductVariant

from django.db.models import Sum

import ipdb


class Command(BaseCommand):
    help = 'collect orders from shopify and place in the Order model'

    def handle(self, *args, **options):
        """
        Reset first
        """
        aggregate_orders = AggregateOrder.objects.all()
        for aggregate_order in aggregate_orders:
            aggregate_order.delete()
        
        aggregates = Aggregate.objects.all()
        for aggregate in aggregates:
            aggregate.delete()
        
        
        # ipdb.set_trace()
        
        """
        Create a new Aggregate
        """
        aggregate = Aggregate()
        aggregate.save()
    
        """
        First, loop through the queryset and save the Orders
        to the AggregateOrder model.
        """
        queryset = Order.objects.all()
        
        print '==== New Aggregate ===='
        
        for order in queryset:
            
            print u'Order: %s' % order
            
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
        print "=== Order Line Items ==="
        for oli in order_line_items:
            print u'%s' % oli
        
        product_variant_kwargs = {
            'shopify_product_variant_id__in': order_line_items.values_list('shopify_product_variant_id', flat=True).distinct()}
            
        product_variants = ProductVariant.objects.filter(**product_variant_kwargs).distinct().order_by('product__vendor')
        print "=== Product Variants ==="
        
        last_vendor = None
        for product_variant in product_variants:
            
            vendor = product_variant.product.vendor
            if vendor != last_vendor:
                print u'===== %s =====' % vendor
                last_vendor = vendor
            
            oli_kwargs = {
                'shopify_product_variant_id': product_variant.shopify_product_variant_id, }
            
            units = order_line_items.filter(**oli_kwargs).aggregate(Sum('quantity'))['quantity__sum']
            grams = product_variant.grams
            order_weight = units * grams
            
            # ipdb.set_trace()
            
            
            aggregate_line_item_kwargs = {
                'aggregate': aggregate,
                'product_variant': product_variant,
                'order_weight': order_weight,
                'order_units': units, }
            
            print u'%s' % product_variant
            print u'           units: %s' % units
            print u'    order_weight: %s' % order_weight
                
            aggregate_line_item = AggregateLineItem(**aggregate_line_item_kwargs)
            try:
                aggregate_line_item.full_clean()
            except ValidationError, e:
                print e
            else:
                aggregate_line_item.save()
            
        
        
        
        
        