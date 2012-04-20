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
        'order',
        'customer',
        'customer_notes',
        'order_notes',
        'order_note_attributes', )

    actions = [
        'packing_item_defaults',
        'generate_invoices',]
        
    def customer(self, obj):
        return str(obj.order.customer).title()
        
    def customer_notes(self, obj):
        return obj.order.customer.note or ''
        
    def order_notes(self, obj):
        return obj.order.note or ''
        
    def order_note_attributes(self, obj):
        note_attributes = eval(obj.order.note_attributes)
        html = ''
        if note_attributes:
            for note in note_attributes:
                html += '<strong>%s</strong>: <span>%s</span><br>' % (note['name'].replace('_', ' ').title(), note['value'].title())
        return html
    order_note_attributes.allow_tags = True

    def generate_invoices(self, request, queryset):
        packing_count = process_packings(queryset)
        packing_errors = len(queryset) - packing_count

        success_message = "Generated invoices for %s packing item(s)" % packing_count
        error_message = "Could not create invoices for %s packing item(s) because they were not fulfilled" % packing_errors
        if packing_count > 0:
            self.message_user(request, success_message)
        if packing_errors > 0:
            self.message_user(request, error_message)


    generate_invoices.short_description = "Generate Invoices from Packing"

    def packing_item_defaults(self, request, queryset):
        
        packing_defaults(queryset)
        self.message_user(request, "Defaults set for %s packing item(s)" % len(queryset))
    packing_item_defaults.short_description = "Set packing item defaults"

admin.site.register(get_model('fulfilment', 'packing'), PackingAdmin)