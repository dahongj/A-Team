from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm
from .models import Feedback
from todo.views import index
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_feedback(request):
	form = FeedbackForm()
	all_reviews = Feedback.objects.all()
	if request.method == 'POST':
		form = FeedbackForm(request.POST,instance=Feedback(manage=request.user))
		if form.is_valid():
			form.save()
			return redirect(index)
	return render(request,'add_feedback.html',{'form': form,'feedback':all_reviews})

