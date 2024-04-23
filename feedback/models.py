from django.db import models
from login.models import CustomUser
from django.conf import settings

# Create your models here.
class Feedback(models.Model):
    manage = models.ForeignKey(CustomUser,on_delete=models.CASCADE, default=None, null= True)
    review = models.TextField(null=False)

    def __str__(self):
        return self.user + " says "+self.review