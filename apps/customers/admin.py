from django.contrib import admin
from django.db.models import get_model


class CustomerInline(admin.StackedInline):
    model = get_model('customers', 'customer')
    extra = 0

class CustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(get_model('customers', 'customer'), CustomerAdmin)
