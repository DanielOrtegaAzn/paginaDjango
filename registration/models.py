from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    is_client = models.BooleanField(default = False)
    is_employee = models.BooleanField(default = False)
    is_admin = models.BooleanField(default=False)
