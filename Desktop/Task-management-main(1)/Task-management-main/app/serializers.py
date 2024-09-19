# serializers.py
from rest_framework import serializers
from .models import Task, Teachers

# Serializer for adding tasks (without teacher details in response)
class AddTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'date', 'start_time', 'end_time', 'subject', 'topic', 'no_of_students', 'standard']

# Serializer for getting task details (with teacher ID and name)
class TaskDetailSerializer(serializers.ModelSerializer):
    teacher_name = serializers.ReadOnlyField(source='teachers.user.username')

    class Meta:
        model = Task
        fields = ['id', 'date', 'start_time', 'end_time', 'subject', 'topic', 'no_of_students', 'standard', 'teacher_name']
