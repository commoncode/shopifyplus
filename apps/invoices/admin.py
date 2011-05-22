from django.contrib import admin
from django.db.models import get_model

class InvoiceItemAdmin(admin.ModelAdmin):
    
    fields = (
        'invoice',
        'packing_item',
        'invoice_weight',
        'invoice_quantity',
        'invoice_unit_weight',
        'invoice_weight_price',
        'invoice_unit_price',)
    
    list_filter = (
        'invoice__signed_off',
        'invoice',
        'packing_item__procurement_item',)
    
    list_display = (
        'invoice',
        'packing_item',
        'invoice_weight',
        'invoice_quantity',
        'invoice_unit_weight',
        'invoice_weight_price',
        'invoice_unit_price',)
        
    list_editable = (
        'invoice_weight',
        'invoice_quantity',
        'invoice_unit_weight',
        'invoice_weight_price',
        'invoice_unit_price',) 
        
    readonly_fields = (
        'invoice',
        'packing_item',)

admin.site.register(get_model('invoices', 'invoiceitem'), InvoiceItemAdmin)

class InvoiceItemInline(admin.StackedInline):
    model = get_model('invoices', 'invoiceitem')
    extra = 0
    
class InvoiceAdmin(admin.ModelAdmin):
    
    fields = (
        'packing',
        'signed_off',
        'signed_off_by',
        'signed_off_key',
        'signed_off_at',)
    
    inlines = [
        InvoiceItemInline, ]
    
    readonly_fields = (
        'packing',) 
        
admin.site.register(get_model('invoices', 'invoice'), InvoiceAdmin)