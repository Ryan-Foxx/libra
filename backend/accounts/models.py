from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(blank=True, max_length=254, verbose_name="email address", unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
