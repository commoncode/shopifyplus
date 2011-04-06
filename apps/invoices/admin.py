from django.contrib import admin
from django.db.models import get_model

class InvoiceItemAdmin(admin.ModelAdmin):
    
    list_filter = (
        'invoice',)
    
    list_display = (
        'invoice',
        'invoice_weight',
        'invoice_weight',
        'invoice_quantity',
        'invoice_unit_weight',
        'invoice_weight_price',
        'invoice_unit_price',  )
        
    list_editable = (
        'invoice_weight',
        'invoice_quantity',
        'invoice_unit_weight',
        'invoice_weight_price',
        'invoice_unit_price', ) 

admin.site.register(get_model('invoices', 'invoiceitem'), InvoiceItemAdmin)

class InvoiceItemInline(admin.StackedInline):
    model = get_model('invoices', 'invoiceitem')
    extra = 0
    
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        InvoiceItemInline, ]
        
admin.site.register(get_model('invoices', 'invoice'), InvoiceAdmin)