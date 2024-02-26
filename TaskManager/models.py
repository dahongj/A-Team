from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from hashlib import sha3_256 as sha

class AppUserManager(BaseUserManager):
    def create_user(self, email, password, last_name, first_name):
        if not email:
            raise ValueError('Email required')
        if not password:
            raise ValueError('Password required')
        email = self.normalize_email(email)
        user = self.model(email = email, last_name = last_name, first_name = first_name)
        user.set_password(password)
        user.save()
        return user
    
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=50,unique=True,primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=32)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = AppUserManager()
    def __str__(self):
        return self.username

class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=50)
    task_desc = models.CharField(max_length=255)
    deadline = models.DateField()
    importance = models.IntegerField()
    is_complete = models.BooleanField()
    completion_date = models.DateField()

    class Meta:
        unique_together = (('task_id', 'user'),)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=0)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = (('task', 'user'),)

class Work_Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    technique = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = (('session_id', 'user', 'task'),)

class Admin(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)


    
        
