from django.http import HttpResponseRedirect
from django.core import management

def product_sync_command(request):
    """
    Sync products using management command

    python manage.py get_products
    """
    management.call_command('get_products', verbosity=0, interactive=False);

    return HttpResponseRedirect('/')