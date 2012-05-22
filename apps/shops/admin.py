import os

from django.contrib import admin
from django.db.models import signals
from django.db.models import get_model
from shops.models import ShopLogo

from shops.utils import fetch_orders as fetch_shop_orders, fetch_products as fetch_shop_products

class ShopAdmin(admin.ModelAdmin):
    
    actions = [
        'fetch_orders',
        'fetch_products', ]
    
    list_display = (
        'title', )
        
    # form = ShopForm
    
    def fetch_orders(self, request, queryset):
        orders = fetch_shop_orders(queryset)
        self.message_user(request, "Fetched orders :: %s" % ', '.join([str(order.order_number) for order in orders]))
    fetch_orders.short_description = "Fetch orders for selected shops"
    
    def fetch_products(self, request, queryset):
        products = fetch_shop_products(queryset)
        self.message_user(request, "Fetched products :: %s" % ', '.join([product.title for product in products]))
    fetch_products.short_description = "Fetch products for selected shops"

admin.site.register(get_model('shops', 'shop'), ShopAdmin)

class ShopLogoAdmin(admin.ModelAdmin):
    list_display = (
            'shop',
            'image'
        )

admin.site.register(ShopLogo, ShopLogoAdmin)


def delete_shoplogo(sender, **kwargs):
    '''
    Deletes image associated with object
    '''
    try:
        old_record = sender.objects.get(pk=kwargs['instance'].pk)
        os.unlink(old_record.image.path)
    except sender.DoesNotExist:
        pass

signals.pre_delete.connect(delete_shoplogo, sender=ShopLogo)
signals.pre_save.connect(delete_shoplogo, sender=ShopLogo)