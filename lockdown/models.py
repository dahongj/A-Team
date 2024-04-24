from django.conf import settings
from django.db import models
from todo.models import TaskList
from login.models import CustomUser


class AllowlistURL(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.url
