from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from ordering.models import OrderItem, Order
from procurement.models import Procurement, ProcurementOrder, ProcurementItem
from products.models import ProductVariant

from django.db.models import Sum

class Command(BaseCommand):
    help = 'collect orders from shopify and place in the Order model'

    def handle(self, *args, **options):
        """
        Reset first
        """
        procurement_orders = ProcurementOrder.objects.all()
        for procurement_order in procurement_orders:
            procurement_order.delete()
        
        procurements = Procurement.objects.all()
        for procurement in procurements:
            procurement.delete()
        
        """
        Create a new Procurement
        """
        procurement = Procurement()
        procurement.save()
    
        """
        First, loop through the queryset and save the Orders
        to the ProcurementOrder model.
        """
        queryset = Order.objects.all()
        
        # print '==== New Procurement ===='
        
        for order in queryset:
            
            # print u'Order: %s' % order
            
            procurement_order = ProcurementOrder(procurement=procurement, order=order)
            try:
                procurement_order.full_clean()
            except ValidationError, e:
                # print u'*** ERROR %s' % e
                # import ipdb; ipdb.set_trace()
                pass
            else:
                procurement_order.save()
            
                """
                If successful, add the Order's OrderItems, Procurementd,
                to the ProcurementItem's
                """
        
        # Find the distinct product_variants    
     
        order_item_kwargs = {
            'order__in': queryset, }
        order_items = OrderItem.objects.filter(**order_item_kwargs) 
        # print "=== Order Line Items ==="
        for oli in order_items:
            # print u'%s' % oli
            pass
        
        product_variant_kwargs = {
            'shopify_product_variant_id__in': order_items.values_list('shopify_product_variant_id', flat=True).distinct()}
            
        product_variants = ProductVariant.objects.filter(**product_variant_kwargs).distinct().order_by('product__vendor')
        # print "=== Product Variants ==="
        
        last_vendor = None
        for product_variant in product_variants:
            
            vendor = product_variant.product.vendor
            if vendor != last_vendor:
                # print u'===== %s =====' % vendor
                last_vendor = vendor
            
            oli_kwargs = {
                'shopify_product_variant_id': product_variant.shopify_product_variant_id, }
            
            units = order_items.filter(**oli_kwargs).aggregate(Sum('quantity'))['quantity__sum']
            grams = product_variant.grams
            order_weight = units * grams
            
            procurement_item_kwargs = {
                'procurement': procurement,
                'product_variant': product_variant,
                'order_weight': order_weight,
                'order_units': units, }
            
            # print u'%s' % product_variant
            # print u'           units: %s' % units
            # print u'    order_weight: %s' % order_weight
                
            procurement_item = ProcurementItem(**procurement_item_kwargs)
            try:
                procurement_item.full_clean()
            except ValidationError, e:
                # print e
                # print u'*** ERROR %s' % e
                # import ipdb; ipdb.set_trace()
                pass
            else:
                procurement_item.save()
            