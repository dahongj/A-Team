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
	return render(request, 'market.html', context)

@login_required
def buy(request, item_id):
	item = Item.objects.get(pk=item_id)
	items = Item.objects.all()
	context = {'items': items}
	if(request.user.points >= item.price):
		request.user.points = request.user.points - item.price
		request.user.save()
		context['message'] = item.name + " has been bought"
		context['itemid'] = item_id
		print(context['message'])
	else:
		context['message'] = "You don't have enough points!"
		context['itemid'] = item_id
		
	return render(request, 'market.html', context)