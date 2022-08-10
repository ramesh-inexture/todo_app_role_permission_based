from rest_framework import serializers
from features.models import Tasklist, Task


class CreateTasklistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasklist
        fields = ['id', 'name', 'created_by']


class UpdateDeleteTasklistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasklist
        fields = ['id', 'name', 'created_by']
        read_only_fields = ['created_by']


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasklist
        fields = ['id', 'list', 'title', 'desc', 'completed']
