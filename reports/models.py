from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from products.models import Product
from areas.models import ProductionLine

hours = ([(str(x),str(x)) for x in range(1,25)])

# Create your models here.
class Report(models.Model):
    day = models.DateField(default=timezone.now)
    start_hour = models.CharField(max_length=2, choices=hours)
    end_hour = models.CharField(max_length=2, choices=hours)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.PositiveIntegerField()
    execution = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    production_line = models.ForeignKey(ProductionLine,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.start_hour} {self.end_hour} {self.production_line}"
    