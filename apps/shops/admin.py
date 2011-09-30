from django.contrib import admin
from django.db.models import get_model

from shops.forms import ShopForm
from shops.utils import fetch_orders as fetch_shop_orders

class ShopAdmin(admin.ModelAdmin):
    
    actions = ['fetch_orders']
    
    list_display = (
        'title', )
        
    # form = ShopForm
    
    def fetch_orders(self, request, queryset):
        orders = fetch_shop_orders(queryset)
        self.message_user(request, "%s orders were fetched" % [order.order_number for order in orders])
    fetch_orders.short_description = "Fetch orders for selected shops"
    
admin.site.register(get_model('shops', 'shop'), ShopAdmin)