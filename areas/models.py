from django.db import models
from profiles.models import Profile
from products.models import Product
# Create your models here.
class ProductionLine(models.Model):
    name = models.CharField(max_length=255)
    team_lead = models.ForeignKey(Profile,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name