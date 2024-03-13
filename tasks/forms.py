from django import forms
from .models import TaskModel
from datetime import datetime

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['taskTitle','taskDescription','importance','deadline']
        widgets = {
            'task_Assign_Date': forms.DateInput(attrs={'type': 'date'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
