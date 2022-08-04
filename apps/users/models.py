from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser

# Register your models here.
class CustomUser(AbstractUser):
    member_id = models.IntegerField(null=True)
