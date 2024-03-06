from django.db import models
from tasks.models import TaskModel
# Create your models here.


class TaskCategory(models.Model):
    categoryName = models.CharField(max_length=255)
    tasks = models.ManyToManyField(TaskModel)

    def __str__(self):
        return self.categoryName
