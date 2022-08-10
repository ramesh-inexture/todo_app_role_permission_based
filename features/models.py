from django.db import models
from django.utils import timezone
from accounts.models import User


class Tasklist(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} | {self.name}'


class Task(models.Model):
    list = models.ForeignKey(Tasklist, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='default')
    desc = models.TextField(max_length=500, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     permissions = [
    #         ("change_task_status", "Can change the status of tasks"),
    #         ("close_task", "Can remove a task by setting its status as closed"),
    #     ]

    def __str__(self):
        return f'{self.list_id} | {self.id} |{self.title}'

    # def get_task_list(self, request, *args, **kwargs):
    #     task_list = Task.objects.filter(list_id=kwargs['list_id'])
    #     return task_list
