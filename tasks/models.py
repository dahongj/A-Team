from django.db import models

# Create your models here.


class TaskModel(models.Model):
    task_id = models.AutoField(primary_key=True)
    taskTitle = models.CharField(max_length=255)
    taskDescription = models.TextField()
    is_completed = models.BooleanField(default=False)
    task_Assign_Date = models.DateField()
    
    #deadline = models.DateField()
    importance = models.IntegerField(default = 0)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.taskTitle
