from django.contrib import admin
from todo.models import TaskList, Feedback

# Register your models here.
admin.site.register(TaskList)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'message']
