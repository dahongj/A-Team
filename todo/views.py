from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from todo.models import TaskList
from todo.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
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

		return render(request, 'todolist.html', {'all_tasks': all_tasks, 'selected_filter': filter})


@login_required
def add_task(request):
	form = TaskForm()
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
		task.save()
	else:
		messages.error(request,("Access Restricted,you are not allowed."))
	return redirect('todolist')

@login_required	
def pending_task(request, task_id):
	task = TaskList.objects.get(pk=task_id)
	task.done = False
	task.save()
	return redirect('todolist')
	
def index(request):
	context = { 'index_text':"Welcome Index Page."}
	return render(request, 'index.html', context)

def completed(request):
		all_tasks = TaskList.objects.filter(manage=request.user)
		paginator = Paginator(all_tasks, 3)
		page = request.GET.get('pg')
		all_tasks = paginator.get_page(page) 
		
		return render(request,'completed.html',{'all_tasks' : all_tasks})

def profile(request):
	return render(request,'profile.html')
