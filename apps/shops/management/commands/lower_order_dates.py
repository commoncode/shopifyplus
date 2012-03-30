from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from datetime import *

from ordering.models import Order       

class Command(BaseCommand):
    args = '<number-of-orders>'
    help = 'lower date time for \'x\' orders. No args for number of possible orders.'

    def handle(self, *args, **options):
        """
        Lower datetime for a number of orders
        """
        
        if len(args) > 0:
            try:
                number_of_orders = int(args[0])
            except Exception, e:
                print "Argument must be a number"
                return
            orders = Order.objects.all()
            if number_of_orders <= orders.count():
                for order in orders[0:number_of_orders]:
                    order.updated_at = order.updated_at - timedelta(seconds=10)
                    order.save() 
                print "Edited", number_of_orders, "orders"
            else:
                print "Can't delete that many orders."
        else:
            print "There are", Order.objects.all().count(), "orders."
            
