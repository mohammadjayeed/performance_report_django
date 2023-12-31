from django.db import models
from profiles.models import Profile
from products.models import Product
# Create your models here.
class ProductionLine(models.Model):
    name = models.CharField(max_length=255)
    team_lead = models.ForeignKey(Profile,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    

    def __str__(self):
        return self.name