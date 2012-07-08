from django.contrib import admin
from django.db.models import get_model


class CustomerInline(admin.StackedInline):
    model = get_model('customers', 'customer')
    extra = 0

class CustomerAdmin(admin.ModelAdmin):
    
    list_display = (
    	'first_name',
    	'last_name',
    	'email',
    	'id',
    	'note')

admin.site.register(get_model('customers', 'customer'), CustomerAdmin)
