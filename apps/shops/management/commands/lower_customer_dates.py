from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from datetime import *

from customers.models import Customer

class Command(BaseCommand):
    args = '<number-of-customers>'
    help = 'lower date time for \'x\' customers`. No args for number of possible customers.'

    def handle(self, *args, **options):
        """
        Lower datetime for a number of customers
        """
        
        if len(args) > 0:
            try:
                number_of_customers = int(args[0])
            except Exception, e:
                print "Argument must be a number"
                return
            customers = Customer.objects.all()
            if number_of_customers <= customers.count():
                for customer in customers[0:number_of_customers]:
                    customer.updated_at = customer.updated_at - timedelta(seconds=10)
                    customer.save() 
                print "Edited", number_of_customers, "customers"
            else:
                print "Can't delete that many customers."
        else:
            print "There are", Customer.objects.all().count(), "customers."
            
