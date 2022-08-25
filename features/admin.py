from django.contrib import admin
from features.models import Task, Tasklist, Notification, Subtask

# Register your models here.
admin.site.register(Task)
admin.site.register(Tasklist)
admin.site.register(Subtask)
admin.site.register(Notification)
