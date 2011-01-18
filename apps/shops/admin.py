from django.contrib import admin
from django.db.models import get_model

class ShopAdmin(admin.ModelAdmin):
    pass

admin.site.register(get_model('shops', 'shop'), ShopAdmin)