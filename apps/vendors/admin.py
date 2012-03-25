from django.contrib import admin
from django.db.models import get_model

class VendorAdmin(admin.ModelAdmin):
    pass

admin.site.register(get_model('vendors', 'vendor'), VendorAdmin)