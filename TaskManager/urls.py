from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home),
]
