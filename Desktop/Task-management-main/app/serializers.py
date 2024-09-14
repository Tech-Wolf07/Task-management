from rest_framework import serializers
from .models import Task

class Taskserializers(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['date','start_time','end_time','subject','topic','no_of_students','standard']