from django import forms
from todo.models import TaskList
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone

class TaskForm(forms.ModelForm):
	CATEGORY_CHOICES = [
        ('Fitness', 'Fitness'),
        ('Nutrition', 'Nutrition'),
        ('College', 'College'),
        ('Mindfulness', 'Mindfulness'),
    ]

	category = forms.ChoiceField(choices=CATEGORY_CHOICES)

	class Meta:
		model = TaskList
		fields = ['task','taskDescription','category','importance', 'points','deadline']
		widgets = {
            'task_Assign_Date': forms.DateInput(attrs={'type': 'date'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
	def clean(self):
		cleaned_data = super().clean()
		task_name = cleaned_data.get('task')
		due_date = cleaned_data.get('deadline')

		if TaskList.objects.filter(task=task_name, deadline=due_date).exists():
			raise forms.ValidationError('The combination of Task and Deadline already exists.')

		return cleaned_data
