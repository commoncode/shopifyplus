from django.contrib import admin
from django.db.models import get_model

class PackingItemAdmin(admin.ModelAdmin):
    
    list_filter = (
        'packing',
        'procurement_item', )
    
    list_display = (
        'packing',
        'order_item',
        'packing_quantity',
        'packing_weight',
        'packing_unit_weight',
        'packing_weight_price',
        'packing_unit_price',
        'fulfilment_weight',
        'fulfilment_quantity',
        'fulfilment_unit_weight',
        'fulfilment_weight_price',
        'fulfilment_unit_price',
        'notes',
        'fulfilled_by',
        'fulfilled_at',
        'fulfilled', )

    list_display_links = (
        'order_item', )
        
    list_editable = (
        'fulfilment_weight',
        'fulfilment_quantity',
        'fulfilment_unit_weight',
        'fulfilment_weight_price',
        'fulfilment_unit_price',
        'notes',
        'fulfilled_by',
        'fulfilled_at',
        'fulfilled', ) 

admin.site.register(get_model('fulfilment', 'packingitem'), PackingItemAdmin)

class PackingItemInline(admin.StackedInline):
    model = get_model('fulfilment', 'packingitem')
    extra = 0
    fields = (
        'packing_quantity',
        'packing_weight',
        'packing_unit_weight',
        'packing_weight_price',
        'packing_unit_price',
        'fulfilment_weight',
        'fulfilment_quantity',
        'fulfilment_unit_weight',
        'fulfilment_weight_price',
        'fulfilment_unit_price',
        'notes',
        'fulfilled_by',
        'fulfilled_at',
        'fulfilled', )
    readonly_fields = (
        'packing_quantity',
        'packing_weight',
        'packing_unit_weight',
        'packing_weight_price',
        'packing_unit_price', ) 
    
class PackingAdmin(admin.ModelAdmin):
    inlines = [
        PackingItemInline, ]
            
    readonly_fields = (
        'order', )   
       
        
admin.site.register(get_model('fulfilment', 'packing'), PackingAdmin)