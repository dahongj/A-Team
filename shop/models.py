from django.db import models
from datetime import date
from login.models import CustomUser
from django.conf import settings

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, default="an item")
    price = models.IntegerField()

    def __str__(self):
        return self.name