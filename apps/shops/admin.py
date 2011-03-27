from django.contrib import admin
from django.db.models import get_model

class ShopAdmin(admin.ModelAdmin):
    
    list_display = (
        'title',
        # 'client',
    )

admin.site.register(get_model('shops', 'shop'), ShopAdmin)