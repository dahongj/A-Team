from django.db import models
from datetime import date

# Create your models here.


class TaskModel(models.Model):
    taskTitle = models.CharField(max_length=255)
    taskDescription = models.TextField(null = True)
    is_completed = models.BooleanField(default=False)
    task_Assign_Date = models.DateField(default = date.today)
    
    deadline = models.DateField(null = True)
    importance = models.IntegerField(default = 0)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.taskTitle
