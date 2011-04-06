from django.contrib import admin
from django.db.models import get_model

from ordering.models import OrderItem
from procurement.models import Procurement, ProcurementOrder, ProcurementItem
from products.models import ProductVariant

from procurement.utils import procurement_orders as process_procurement_orders

def procurement_orders(modeladmin, request, queryset):
    process_procurement_orders(queryset)
procurement_orders.short_description = "Create procurement items for selected orders"

class OrderItemAdmin(admin.StackedInline):
    model = get_model('ordering', 'orderitem')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemAdmin, ]
        
    actions = [procurement_orders]

admin.site.register(get_model('ordering', 'order'), OrderAdmin)