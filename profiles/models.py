from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(blank=True)
    website = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"