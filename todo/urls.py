from django.urls import path, include
from todo import views

urlpatterns = [
    path('',views.todolist,name='todolist'),
    path('completed',views.completed,name='completed'),
    path('delete/<task_id>',views.delete_task,name='delete_task'),
    path('add_task',views.add_task,name='add_task'),
    path('edit/<task_id>',views.edit_task,name='edit_task'),
    path('complete/<task_id>',views.complete_task, name= 'complete_task'),
    path('pending/<task_id>',views.pending_task, name='pending_task'),
    path('profile',views.profile, name='profile'),
    path('shop',views.shop, name='shop'),
    path('lockdown/', include(('lockdown.urls','lockdown'), namespace='lockdown')),
]