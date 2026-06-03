from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    rating = models.IntegerField(default = 0)
    streak = models.IntegerField(default = 0)

