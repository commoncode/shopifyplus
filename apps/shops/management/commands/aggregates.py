from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from orders.models import Order

class Command(BaseCommand):
    help = 'compile Procurements'

    def handle(self, *args, **options):
        """
        Procurements
        """

        shop = Shop.objects.get()
        shop.connect()
        
        orders = shop.orders()
    
        """
        Collect orders and order items into our
        django models.
        """
    
        for order in list(orders):
            
            
            """
            Parse the order and save it
            """
            order_kwargs = {
            
                
            
            }
            
            order = Order(**order_kwargs)
                        
            try:
                article.full_clean()
                # pass
            except ValidationError, e:
                # Do something based on the errors contained in e.message_dict.
                # Display them to a user, or handle them programatically.
                print e
            else:
                """
                success
                """
                print order