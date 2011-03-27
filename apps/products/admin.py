from django.contrib import admin
from django.db.models import get_model

class ProductImageInline(admin.StackedInline):
    extra = 1
    sortable_field_name = "position"
    
class ProductVariantInline(admin.StackedInline):
    extra = 0
    model = get_model('products', 'productvariant')

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductVariantInline, ]
        
    list_display = (
        'title',
        'vendor', )
    list_editable = (
        'vendor', )
            

admin.site.register(get_model('products', 'product'), ProductAdmin)