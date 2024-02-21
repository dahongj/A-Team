from django.contrib import admin
from .models import User,Tasks, Feedback, Work_Session

# Register your models here.
admin.site.register(User)
admin.site.register(Tasks)
admin.site.register(Feedback)
admin.site.register(Work_Session)