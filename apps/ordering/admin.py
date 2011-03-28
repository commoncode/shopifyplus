from django.contrib import admin
from django.db.models import get_model

from ordering.models import OrderLineItem
from aggregates.models import Aggregate, AggregateOrder, AggregateLineItem
from products.models import ProductVariant

from aggregates.utils import aggregate_orders as process_aggregate_orders

def aggregate_orders(modeladmin, request, queryset):
    process_aggregate_orders(queryset)
aggregate_orders.short_description = "Aggregate selected orders"

class OrderLineItemAdmin(admin.StackedInline):
    model = get_model('ordering', 'orderlineitem')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderLineItemAdmin, ]
        
    actions = [aggregate_orders]

admin.site.register(get_model('ordering', 'order'), OrderAdmin)