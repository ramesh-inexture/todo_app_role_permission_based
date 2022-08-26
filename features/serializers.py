from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from features.models import Tasklist, Task, Notification, Subtask


class CreateTasklistSerializer(serializers.ModelSerializer):
    """Serializer for Creating list in Tasklist Model"""
    class Meta:
        model = Tasklist
        fields = ['id', 'name', 'created_by']


class UpdateDeleteTasklistSerializer(serializers.ModelSerializer):
    """serializer of Update and delete TaskList in TasklistModel"""
    class Meta:
        model = Tasklist
        fields = ['id', 'name', 'created_by']
        read_only_fields = ['created_by']


class CreateTaskSerializer(serializers.ModelSerializer):
    """Serializer for Creating Task in Task Model"""
    class Meta:
        model = Task
        fields = ['id', 'list', 'title', 'desc', 'completed']


class ManageTaskSerializer(serializers.ModelSerializer):
    """Serializer of Managing Task or Subtasks of Task models"""
    class Meta:
        model = Task
        fields = ['id', 'list', 'title', 'desc', 'completed', 'is_subtask']
        extra_kwargs = {
            "id": {"read_only": True},
            "list": {"read_only": True},
            "is_subtask": {"read_only": True},
        }


class CreateSubtaskSerializer(serializers.ModelSerializer):
    """Serializer for creating subtask in TaskModel"""
    class Meta:
        model = Task
        fields = ['id', 'list', 'title', 'desc', 'completed', 'is_subtask']


class SubtaskModelSerializer(serializers.ModelSerializer):
    """Model Serializer Of Task (parent_id) and Sub_task (child_id) in Subtask Table"""
    class Meta:
        model = Subtask
        fields = ['task', 'sub_task']


class SearchTaskSerializer(serializers.ModelSerializer):
    """Serializer to Search Task or Subtask by their title name """
    class Meta:
        model = Task
        fields = ['id', 'list', 'title', 'desc', 'completed']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification Model"""
    class Meta:
        model = Notification
        fields = ['title', 'task', 'notification', 'receiver', 'sender', 'created_at']


class TaskModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'desc', 'created_at', 'completed', 'is_subtask']


class RetrieveTasklistSerializer(serializers.ModelSerializer):
    Tasks = serializers.SerializerMethodField(read_only=True)

    def get_Tasks(self, obj):
        Tasks = [i for i in obj.Tasks.filter(is_subtask=False)]
        return TaskModelSerializer(Tasks, many=True).data

    class Meta:
        model = Tasklist
        fields = ['name', 'created_by', 'created_at', 'Tasks']


class TaskRetrieveSerializer(serializers.ModelSerializer):
    sub_tasks = serializers.SerializerMethodField(read_only=True)

    def to_representation(self, obj):
        """
        If this serializer is used for task object(which is subtask) then remove 'sub_tasks' attribute.
        :param obj: Task object
        :return: representation of each field as dictionary
        """
        result = super(TaskRetrieveSerializer, self).to_representation(obj)
        if obj.is_subtask:
            result.pop('sub_tasks')
        return result

    def get_sub_tasks(self, obj):
        sub_tasks = [i.sub_task for i in obj.sub_tasks.all()]
        return TaskModelSerializer(sub_tasks, many=True).data

    class Meta:
        model = Task
        fields = ['id','title', 'desc', 'created_at', 'completed', 'is_subtask', 'list', 'sub_tasks']



