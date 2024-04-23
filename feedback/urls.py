from django.urls import path
from feedback import views

urlpatterns = [
    path('',views.add_feedback,name='add_feedback'),
]