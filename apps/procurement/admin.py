from django.contrib import admin
from django.db.models import get_model


class ProcurementItemAdmin(admin.ModelAdmin):
    list_filter = (
        'procurement',
        'product_variant__product__vendor',
        )
        
    list_display = (
        'product_variant',
        'order_units',
        'order_weight',
        'procurement_weight',
        'procurement_quantity',
        'procurement_unit_weight',
        'procurement_weight_price',
        'procurement_unit_price',
        'procured',  )
        
    list_editable = (
        'procurement_weight',
        'procurement_quantity',
        'procurement_unit_weight',
        'procurement_weight_price',
        'procurement_unit_price',
        'procured', )
        
admin.site.register(get_model('procurement', 'procurementitem'), ProcurementItemAdmin)    
    
class ProcurementItemInline(admin.StackedInline):
    model = get_model('procurement', 'procurementitem')
    extra = 0

class ProcurementAdmin(admin.ModelAdmin):
    inlines = [
        ProcurementItemInline, ]
        
    list_display = (
        'created_at',)
        
    # list_editable = (
    #     'shops', )

admin.site.register(get_model('procurement', 'procurement'), ProcurementAdmin)

# class ProcurementOrderAdmin(admin.ModelAdmin):
#     pass
# 
# admin.site.register(get_model('Procurements', 'Procurementorder'), ProcurementOrderAdmin)