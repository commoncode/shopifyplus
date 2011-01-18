from django.contrib import admin
from django.db.models import get_model

class ProductImageInline(admin.StackedInline):
    extra = 1
    sortable_field_name = "position"

class ProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(get_model('products', 'product'), ProductAdmin)