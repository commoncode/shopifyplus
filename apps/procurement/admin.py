from django.contrib import admin
from django.db.models import get_model

from procurement.utils import procurement_item_defaults as set_procurement_item_defaults

class ProcurementItemAdmin(admin.ModelAdmin):
    list_filter = (
        'procurement',
        'product_variant__product__vendor', )
        
    list_display = (
        'product_variant',
        'order_units',
        'order_weight',
        'procurement_weight',
        'procurement_quantity',
        'procurement_unit_weight',
        'procurement_weight_price',
        'procurement_unit_price',
        'procured', )
        
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
    
    actions = ['procurement_item_defaults']
    
    inlines = [
        ProcurementItemInline, ]
        
    list_display = (
        'created_at',
        'procurement_csv', )
        
    def procurement_csv(self, obj):
        return u'Download <a href="%s">csv</a>' % (
            obj.get_csv_url())
    procurement_csv.allow_tags=True
    procurement_csv.short_description= 'CSV'    
        
    def procurement_item_defaults(self, request, queryset):
        procurement_items = set_procurement_item_defaults(queryset)
        self.message_user(request, "Defaults set for %s procurement item(s)" % len(procurement_items))
    procurement_item_defaults.short_description = "Set procurement item defaults"

admin.site.register(get_model('procurement', 'procurement'), ProcurementAdmin)

# class ProcurementOrderAdmin(admin.ModelAdmin):
#     pass
# 
# admin.site.register(get_model('Procurements', 'Procurementorder'), ProcurementOrderAdmin)