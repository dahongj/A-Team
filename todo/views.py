from django.shortcuts import render, redirect
from django.http import HttpResponse
from todo.models import TaskList
from login.models import CustomUser
from todo.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from celery import shared_task
import json

@login_required	
def index(request):
	all_tasks = TaskList.objects.filter(manage=request.user, done=0)
	imp_tasks = TaskList.objects.filter(manage=request.user).order_by('importance')
	com_tasks = TaskList.objects.filter(manage=request.user, done = 1)

	now = timezone.now()
	alert_message = ""
	for task in all_tasks:
		remaining_time = task.deadline - now.date()
		if remaining_time.days <= 1:
			alert_message = "Some tasks have a deadline less than a day!"
			break

	context = { 'index_text':"Welcome Index Page.", 'all_tasks': all_tasks, 'imp_tasks': imp_tasks, 'com_tasks': com_tasks, 'alert_message': alert_message}
	return render(request, 'index.html', context)

@login_required
def todolist(request):
	# Check if the form has been submitted
	if request.method == "POST":
		form = TaskForm(request.POST or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.manage = request.user
			instance.save()
			messages.success(request, ("New Task Added!"))
			return redirect('todolist')
	else:
		task_filter = request.GET.get('filter', 'all')
		filter = ""
		if task_filter == 'completed':
			all_tasks = TaskList.objects.filter(manage=request.user, done = 1)
			paginator = Paginator(all_tasks, 3)
			page = request.GET.get('pg')
			all_tasks = paginator.get_page(page)
			filter = 'completed'

		elif task_filter == 'incomplete':
			all_tasks = TaskList.objects.filter(manage=request.user, done=0)
			filter = 'incomplete'
		elif task_filter == 'due_date':
			all_tasks = TaskList.objects.filter(manage=request.user).order_by('-deadline')
			filter = 'due_date'
		elif task_filter == 'priority':
			all_tasks = TaskList.objects.filter(manage=request.user).order_by('importance')
			filter = 'priority'
		else:
			all_tasks = TaskList.objects.filter(manage=request.user)
			filter = 'all'

		todo_tasks = TaskList.objects.filter(manage=request.user, done=0)
		completed_tasks = TaskList.objects.filter(manage=request.user, done = 1)
		priority_tasks = TaskList.objects.filter(manage=request.user, done=0, importance__lt=10)

		for task in priority_tasks:
			if 0 <= task.importance <= 2:
				task.color = 'red'
			elif 3 <= task.importance <= 6:
				task.color = 'yellow'
			elif 7 <= task.importance <= 10:
				task.color = 'green'

		return render(request, 'todolist.html', {'all_tasks': all_tasks, 'selected_filter': filter, 'todo_tasks': todo_tasks, 'completed_tasks': completed_tasks, 'priority_tasks': priority_tasks})


@login_required
def add_task(request):
	task_name = request.GET.get('task_name', '')
	category = request.GET.get('category', '')
	form = TaskForm(initial={'task': task_name, 'category': category})
	if request.method == 'POST':
		form = TaskForm(request.POST,instance=TaskList(manage=request.user))
		if form.is_valid():
			form.save()
			return redirect(todolist)
	return render(request,'addtask.html',{'form': form})


@login_required
def delete_task(request, task_id):
	task =TaskList.objects.get(pk=task_id)
	if task.manage == request.user:
		task.delete()
	else:
		messages.error(request,("Access Restricted,you are not allowed."))	
	return redirect('todolist')

@login_required
def edit_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, ("Task Edited!"))
            return redirect('todolist')
    else:
        form = TaskForm(instance=task)
    return render(request, 'addtask.html', {'form': form, 'task_id': task_id})

@login_required		
def complete_task(request, task_id):
	task = TaskList.objects.get(pk=task_id)
	if task.manage == request.user:
		task.done = True
		user = request.user
		user.points += task.points
		user.save()
		task.save()
	else:
		messages.error(request,("Access Restricted,you are not allowed."))
	return redirect('todolist')

@login_required		
def shop(request):
	return render(request, 'shop.html')

@login_required	
def pending_task(request, task_id):
	task = TaskList.objects.get(pk=task_id)
	user = request.user
	user.points -= task.points
	user.save()
	task.done = False
	task.save()
	return redirect('todolist')

def completed(request):
		all_tasks = TaskList.objects.filter(manage=request.user, done = 0)
		paginator = Paginator(all_tasks, 3)
		page = request.GET.get('pg')
		all_tasks = paginator.get_page(page)
		return render(request,'completed.html',{'all_tasks' : all_tasks})


def profile(request):
	total_tasks = len(TaskList.objects.filter(manage=request.user))
	completed = len(TaskList.objects.filter(manage=request.user, done = 1))
	if total_tasks == 0:
		total_tasks = 1
	user = request.user
	progress_data = {'completed': (completed/total_tasks) * 100, 'remaining': ((total_tasks-completed)/total_tasks) * 100}
	full_name = f"{user.first_name} {user.last_name}".strip() if user.first_name and user.last_name else ""

	context = {
        'email': user.email,
        'name': full_name,
        'progress_data': json.dumps(progress_data),
		'fraction': f"{completed}/{total_tasks}",
		'percentage': (completed/total_tasks) * 100,
        'total_points': user.points,
	}
	return render(request, 'profile.html', context)

@shared_task
def update_task_priorities(request):
    todo_tasks = TaskList.objects.filter(manage=request.user, done=0)

    now = timezone.now()

    for task in todo_tasks:
        remaining_time = task.deadline - now.date()

        if remaining_time.days <= 3:
            task.importance = max(task.importance - 1, 1)
        else:
            pass

        task.save()
