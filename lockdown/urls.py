from django.urls import path
from lockdown.views import start_lockdown,end_lockdown,manage_urls, delete_url
urlpatterns = [
    path('',start_lockdown, name='lockdown'),
    path('exit_lockdown/',end_lockdown, name='end_lockdown'),
    path('manage-urls/',manage_urls, name='manage-urls'),
    path('delete-url/<int:url_id>/', delete_url, name='delete-url'),
]
