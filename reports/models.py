from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    