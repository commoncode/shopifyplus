from django.contrib import admin
from django.db.models import get_model
from fulfilment.models import PackingItem
from invoices.utils import process_packings
from fulfilment.utils import packing_defaults

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

    def _order_item(self, obj):
        return obj.order_item

admin.site.register(get_model('fulfilment', 'packingitem'), PackingItemAdmin)

class PackingItemInline(admin.TabularInline):
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

    actions = [
        'packing_item_defaults',
        'generate_invoices',]

    def generate_invoices(self, request, queryset):
        process_packings(queryset)
    generate_invoices.short_description = "Generate Invoices from Packing"

    def packing_item_defaults(self, request, queryset):
        
        packing_defaults(queryset)
        self.message_user(request, "Defaults set for %s packing item(s)" % len(queryset))
    packing_item_defaults.short_description = "Set packing item defaults"

admin.site.register(get_model('fulfilment', 'packing'), PackingAdmin)