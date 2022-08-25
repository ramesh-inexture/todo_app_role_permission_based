from django.db import models
from django.utils import timezone
from accounts.models import User


class Tasklist(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Tasklist {self.id}'


class Task(models.Model):
    list = models.ForeignKey(Tasklist, on_delete=models.CASCADE, related_name="Tasks")
    title = models.CharField(max_length=255, default='default')
    desc = models.TextField(max_length=500, blank=True)
    is_subtask = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # this is how we can create permission in Permission Table
    # class Meta:
    #     permissions = [
    #         ("change_task_status", "Can change the status of tasks"),
    #         ("close_task", "Can remove a task by setting its status as closed"),
    #     ]

    def __str__(self):
        return f'{self.list} | Task {self.id}'


class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="sub_tasks")
    sub_task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="parent_task")

    def __str__(self):
        return f'{self.id} |{self.task} | Subtask {self.sub_task.id}'


class Notification(models.Model):
    title = models.CharField(max_length=255)
    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL)
    notification = models.CharField(max_length=255)
    receiver = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='receiver')
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='sender')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'
