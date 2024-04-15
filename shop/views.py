from django.shortcuts import render, redirect
from django.http import HttpResponse
from todo.models import TaskList
from todo.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import *

@login_required
def shop(request):
	items = Item.objects.all()
	context = {'items': items}
	return render(request, 'shop.html', context)