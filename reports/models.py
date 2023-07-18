from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from products.models import Product
from areas.models import ProductionLine
from category.models import Category


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
    production_line = models.ForeignKey(ProductionLine,on_delete=models.CASCADE, related_name='pl')

    def __str__(self):
        return f"{self.start_hour} {self.end_hour} {self.production_line}"
    
class ProblemReported(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    problem_id = models.CharField(max_length=12, unique=True, blank=True)
    breakdown = models.SmallIntegerField()
    public = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category.name

    class Meta:
        verbose_name = 'Problem Reported'
        verbose_name_plural = 'Problems Reported'

    