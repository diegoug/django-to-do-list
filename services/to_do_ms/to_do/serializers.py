from rest_framework import serializers

from .models import Task


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['user', 'title','description','status']
