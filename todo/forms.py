from django import forms
from todo.models import TaskList
from datetime import date

class TaskForm(forms.ModelForm):
	class Meta:
		model = TaskList
		fields = ['task','taskDescription','importance','deadline']
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