from django import forms
from .models import TaskModel
from datetime import datetime

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = '__all__'
        widgets = {
            'task_Assign_Date': forms.DateInput(attrs={'type': 'date'}),
        }
