from django.shortcuts import render, redirect, get_object_or_404
from lockdown.middleware import LockedBrowserMiddleware
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from todo import views
from todo.models import TaskList
from lockdown.forms import WebsiteForm
from lockdown.models import AllowlistURL



@login_required
def start_lockdown(request,task_id):
    task = TaskList.objects.get(pk=task_id)
    user = task.manage
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            new_url = form.save(commit=False)
            new_url.user = request.user
            new_url.save()
            request.session['is_in_lockdown'] = True
            return render(request,'locked.html')
    else:
        form = WebsiteForm(instance=task)
    return render(request, 'manage_urls.html',{'form': form, 'user': user})

@login_required
def end_lockdown(request):
    # Clear the session flag
    out = request.session.pop('is_in_lockdown')
    return redirect('todolist')


@login_required
@permission_required('is_in_lockdown', raise_exception=True)
def navigate(request):
    url = request.GET.get('url', '')
    if url in LockedBrowserMiddleware.allowed_hosts:
        return redirect(url)
    elif url in LockedBrowserMiddleware.forbidden_hosts:
        messages.warning("Stay Focus!")
        return redirect('locked_page')
    
@login_required
def manage_urls(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            new_url = form.save(commit=False)
            new_url.user = request.user
            new_url.save()
            return redirect('manage-urls')
    else:
        form = WebsiteForm()
    urls = AllowlistURL.objects.filter(user=request.user)
    return render(request, 'manage_urls.html', {'form': form, 'urls': urls})

login_required
def delete_url(request, url_id):
    url = AllowlistURL.objects.get(id=url_id, user=request.user)
    url.delete()
    return redirect('manage-urls')