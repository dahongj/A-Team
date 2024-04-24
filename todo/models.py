from django.db import models
from datetime import date
from login.models import CustomUser
from django.conf import settings

# Create your models here.
class TaskList(models.Model):
	manage = models.ForeignKey(CustomUser,on_delete=models.CASCADE, default=None, null= True)

	CATEGORY_CHOICES = [
        ('Fitness', 'Fitness'),
        ('Nutrition', 'Nutrition'),
        ('College', 'College'),
        ('Mindfulness', 'Mindfulness'),
    ]

	task = models.CharField(max_length=300)
	done = models.BooleanField(default=False)
	taskDescription = models.TextField(null = True)
	task_Assign_Date = models.DateField(default = date.today)
	deadline = models.DateField(null = True)
	importance = models.IntegerField(default = 0)
	points = models.IntegerField(default = 0)
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Fitness')

	def __str__(self):
		return self.task + "-" + str(self.done)