import requests

from django.core import management

from celery import task

@task()
def shops_support_commands_task():

    # TODO: these could be chained with callbacks.
    management.call_command('reset', 'customers', noinput=True, verbosity=0, interactive=False);
    management.call_command('reset', 'products', noinput=True, verbosity=0, interactive=False);
    management.call_command('get_products', verbosity=0, interactive=False);
    management.call_command('reset', 'ordering', noinput=True, verbosity=0, interactive=False);
    management.call_command('get_orders', verbosity=0, interactive=False);
    management.call_command('reset', 'procurement', noinput=True, verbosity=0, interactive=False);
    management.call_command('create_procurement_items', verbosity=0, interactive=False);

    management.call_command('procurement_item_defaults', verbosity=0, interactive=False);
    management.call_command('process_procurement_orders', verbosity=0, interactive=False);
    management.call_command('packing_item_defaults', verbosity=0, interactive=False);
    management.call_command('create_invoices', verbosity=0, interactive=False);

    r = requests.get('http://www.smsglobal.com/http-api.php?action=sendsms&user=dalidada&password=maximus&from=ShopifyPlus&to=0402231007&text=Procurements%20Complete')
    print r.text