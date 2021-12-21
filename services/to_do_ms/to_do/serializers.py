from rest_framework import serializers

from .models import Task


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id' ,'user', 'title','description','status']
