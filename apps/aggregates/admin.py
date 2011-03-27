from django.contrib import admin
from django.db.models import get_model


class AggregateLineItemAdmin(admin.ModelAdmin):
    list_filter = (
        'aggregate',
        'product_variant__product__vendor',
        )
        
    list_display = (
        'product_variant',
        # 'product_variant__product__vendor',
        'order_units',
        'order_weight', )
        
admin.site.register(get_model('aggregates', 'aggregatelineitem'), AggregateLineItemAdmin)    
    
class AggregateLineItemAdmin(admin.StackedInline):
    model = get_model('aggregates', 'aggregatelineitem')
    extra = 0

class AggregateAdmin(admin.ModelAdmin):
    inlines = [
        AggregateLineItemAdmin, ]

admin.site.register(get_model('aggregates', 'aggregate'), AggregateAdmin)

class AggregateOrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(get_model('aggregates', 'aggregateorder'), AggregateOrderAdmin)