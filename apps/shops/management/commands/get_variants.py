from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from shopifyable.utils import element_kwargs
from shops.models import Shop
from products.models import Product, ProductVariant


import ipdb


def fetch_variants(product):
        
    product.variants()
    
    for _variant in list(product._variants):
        
        variant = ProductVariant(product=product, **element_kwargs(ProductVariant, _variant))
        try:
            variant.full_clean()
        except ValidationError, e:
            # Do something based on the errors contained in e.message_dict.
            # Display them to a user, or handle them programatically.
            print e
        else:
            variant.save()
            print variant

class Command(BaseCommand):
    help = 'collect variants from shopify and place in the ProductVariant model'

    def handle(self, *args, **options):
        """
        Variants
        """

        shop = Shop.objects.get()
        products = Product.objects.filter(shop=shop)
        for product in products:
            fetch_variants(product)

        