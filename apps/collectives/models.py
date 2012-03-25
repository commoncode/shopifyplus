from django.db import models

class Collective(models.Model):
    """
    A Collective, or product collective
    determines how a product should be sold,
    referring to its packaging and units 
    'sold by'
    """
    
    
    name = models.CharField(max_length=100)
    
    sold_by_weight = models.BooleanField()
    sold_by_quantity = models.BooleanField()
    sold_by_cost = models.BooleanField()

