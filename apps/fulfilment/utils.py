from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User

from ordering.models import OrderItem, Order
from procurement.models import Procurement, ProcurementOrder, ProcurementItem
from products.models import ProductVariant
from fulfilment.models import Packing, PackingItem


from django.db.models import Sum

import math
import datetime

def calculate_packing_variable(procurement_order_variable,
                               procurement_variable, 
                               order_variable):
    """
    Calculates the packing_variable on a spread even basis,
    if, the procurment variable is less that what was ordered.
    
    E.g. 
    
        The order_weight was 10kg, tho only 9kg was available
        
        So, 
            spread 9kg evenly, as a ratio, i.e. 9/10 across
            the individual order_item.order_weight
            
        Thus,
            Order #1000 order_weight = 7000g
            Order #1001 order_weight = 3000g
            Total 'Order Weight' = 100000g
            Total 'Procument Weight' = 9000g
            
            So #1000 gets 7 * 9 / 10 = 6300g &
               #1001 gets 3 * 9 / 10 = 2700g
    """
    pov = procurement_order_variable
    prv = procurement_variable
    orv = order_variable
    
    try:
        if prv < pov and orv:
            pav = prv / pov * orv
        elif prv >= pov and orv:
            pav = orv
        else:
            pav = None
    except:
        pav = None
    
    if pav:
        return int(math.floor(float(pav))) # Integer's only
    else:
        return None
    

def process_procurement_orders(queryset):

    """
    Given a Procurement create a set of Packings & Packing Items
    with the related Orders, and adjusted by global changes
    found in the ProcurementItems
    """
    
    procurements = queryset
    
    for procurement in procurements:
        
        procurement_orders = ProcurementOrder.objects.filter(procurement=procurement)
        
        for procurement_order in procurement_orders:
            
            order_items = OrderItem.objects.filter(order=procurement_order.order)
            
            packing = Packing(order=procurement_order.order)
            packing.save()
            
            for order_item in order_items:
                
                try:
                    product_variant = ProductVariant.objects.get(shopify_product_variant_id=order_item.shopify_product_variant_id)
                except Exception, e:
                    print u'*** ERROR :: Product variant not found for order item :: %s' % order_item
                    try:
                        product_variants = ProductVariant.objects.filter(title__startswith=order_item.variant_title[0:8])
                        print '    searched on :: %s' % order_item.variant_title[0:8]
                        print '    found %s product variants' % product_variants.count()
                        print '    taking %s' % product_variants[0]
                        product_variant = product_variants[0]
                    except IndexError:
                        print u'*** STILL NOT FOUND :: Product variant not found for order item :: %s' % order_item
                    except TypeError:
                        print u'    ++++ NO REPLACEMENT FOUND ++++'
                    else:
                        print u'    ==== SUBSTITUTE VARIANT USED ===='
                        
                else:
                
                    procurement_item_kwargs = {
                        'procurement': procurement,
                        'product_variant': product_variant, }
                    
                    try:
                        procurement_item = ProcurementItem.objects.get(**procurement_item_kwargs)
                    except ObjectDoesNotExist:
                        # Should exist unless deleted from underneath
                        print u'*** ERROR %s' % e
                    else:
                    
                        order_weight = order_item.grams * order_item.quantity    
                        packing_weight = calculate_packing_variable(
                            procurement_item.order_weight, 
                            procurement_item.procurement_weight, 
                            order_weight)
                    
                        packing_quantity = calculate_packing_variable(
                            procurement_item.order_quantity, 
                            procurement_item.procurement_quantity, 
                            order_item.quantity)
                
                        packing_item_kwargs = {
                            'packing': packing,
                            'order_item': order_item,
                            'procurement_item': procurement_item,
                            'packing_weight': packing_weight,        
                            'packing_quantity': packing_quantity,
                            'packing_unit_weight': procurement_item.procurement_unit_weight,
                            'packing_weight_price': procurement_item.procurement_weight_price,
                            'packing_unit_price': procurement_item.procurement_unit_price, }
                        packing_item = PackingItem(**packing_item_kwargs)
                        try:
                            packing_item.full_clean()
                        except ValidationError, e:
                            print u'*** ERROR %s' % e
                        else:
                            packing_item.save()
                            print packing_item
                    
def packing_item_defaults(queryset):
    """
    For each PackingItem set the fulfilment values
    to equal the packing values.
    """
    packing_items = queryset
    
    for packing_item in packing_items:
        
        product_variant = ProductVariant.objects.get(shopify_product_variant_id=packing_item.order_item.shopify_product_variant_id)
        try:
            fulfilment_weight_price = float(1000.00) / float(product_variant.grams) * product_variant.price
        except:
            fulfilment_weight_price = None
            
        packing_item.fulfilment_weight = packing_item.packing_weight
        packing_item.fulfilment_quantity = packing_item.packing_quantity
        packing_item.fulfilment_unit_weight = product_variant.grams
        packing_item.fulfilment_weight_price = fulfilment_weight_price
        packing_item.fulfilment_unit_price = product_variant.price
        packing_item.fulfilled = True
        packing_item.fulfilled_by = User.objects.get(pk=1)
        packing_item.fulfilled_at = datetime.datetime.now()
        packing_item.save()
                    
def packing_item_csv(queryset):
    
    """
    Dump all the packing items to a csv
    """
    packing_items = queryset
    print 'Number, SKU, Quantity, Product, Order Weight, $ per kg, Item Price, Order Cost, Adjustments'
    for packing_item in packing_items:
        
        product_variant = ProductVariant.objects.get(shopify_product_variant_id=packing_item.order_item.shopify_product_variant_id)
        
        order_number = packing_item.order_item.order.name
        sku = packing_item.order_item.sku
        quantity = packing_item.packing_quantity if product_variant.option2 not in ['loose'] else ' '
        product = u'%s :: %s' % (product_variant.product, product_variant.option1)
        # product_variant = product_variant.option1
        # item_weight = packing_item.packing_unit_weight / float(1000.000) if product_variant.option2 in ['single',] else ' '
        order_weight = packing_item.packing_weight / float(1000.000) if packing_item.packing_weight else ' '
        weight_price = packing_item.packing_weight_price if packing_item.packing_weight_price else ' '
        item_price = packing_item.packing_unit_price if product_variant.option2 not in ['loose'] else ' '
        order_cost = packing_item.packing_unit_price * packing_item.packing_quantity
        
        
        print '%s,%s,%s,%s,%s,%s,%s,%s,' % (
            order_number,
            sku,
            quantity,
            product, 
            # product_variant, 
            # item_weight, 
            order_weight, 
            weight_price, 
            item_price, 
            order_cost)
    
    
    
    
    
    
            
