vhosts = {
    # Shopify Plus
    'shopifyplus.commoncode.com.au': {
        'hosts': ['shopifyplus.commoncode.com.au'], # could be a callable returning a list of hosts
        'manage': './manage.py',
        'settings': 'settings',
        'requirements': 'requirements/project.txt',
        'celery': True,
    },
}
