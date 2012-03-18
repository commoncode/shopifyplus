from django.contrib import admin
from django.db.models import get_model

from customers.admin import CustomerInline
from ordering.models import OrderItem
from procurement.models import Procurement, ProcurementOrder, ProcurementItem
from products.models import ProductVariant

from procurement.utils import procurement_orders as process_procurement_orders

def procurement_orders(modeladmin, request, queryset):
    process_procurement_orders(queryset)
procurement_orders.short_description = "Create procurement items for selected orders"

class OrderItemInline(admin.StackedInline):
    model = get_model('ordering', 'orderitem')
    extra = 0
    
class ShippingLineInline(admin.StackedInline):
    model = get_model('ordering', 'shippingline')
    extra = 0
    
class ShippingAddressInline(admin.StackedInline):
    model = get_model('ordering', 'shippingaddress')
    extra = 0
    
class BillingAddressInline(admin.StackedInline):
    model = get_model('ordering', 'billingaddress')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        CustomerInline,
        BillingAddressInline,
        ShippingAddressInline,
        OrderItemInline,
        ShippingLineInline, ]
        
    actions = [procurement_orders]

admin.site.register(get_model('ordering', 'order'), OrderAdmin)