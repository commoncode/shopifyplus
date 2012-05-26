from django.http import HttpResponseRedirect
from django.core import management

def ordering_sync_command(request):
    """
    Sync orders using management command

    python manage.py get_orders
    """
    management.call_command('reset', 'ordering', noinput=True, verbosity=0, interactive=False);
    management.call_command('get_orders', verbosity=0, interactive=False);

    return HttpResponseRedirect('/')