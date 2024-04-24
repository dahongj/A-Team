from django import forms
from todo.models import TaskList, Feedback
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
		category = cleaned_data.get('category')
		imp = cleaned_data.get('importance')
		points = cleaned_data.get('points')
		due_date = cleaned_data.get('deadline')

		# Check if the deadline is in the past
		if due_date and (due_date < timezone.now().date()):
			raise forms.ValidationError({
                'deadline': 'The deadline cannot be in the past.'
            })
		# Check if the task with the same name and deadline already exists
		if TaskList.objects.filter(task=task_name, deadline=due_date, category = category, importance = imp, points = points).exists():
			raise forms.ValidationError('This exact same task already exists!!!')

		return cleaned_data


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
