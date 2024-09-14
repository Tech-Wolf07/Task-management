from django.db import models

# Create your models here.
from django.contrib.auth.models import User



class Teachers(models.Model):
    name = models.CharField(max_length=100,default='')
    school = models.CharField(max_length=100,default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE,default='')     
    def __str__(self):              
        return self.user.username
    
class Coordinator(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ForeignKey(Teachers, on_delete=models.SET_NULL,null=True)
    def __str__(self):              
        return self.name


class Task(models.Model):
      date = models.DateField()
      start_time = models.TimeField()
      end_time = models.TimeField()
      subject = models.CharField(max_length=50)
      topic = models.CharField(max_length=100, default=None)
      no_of_students = models.PositiveIntegerField(null=True)
      standard = models.IntegerField(null=True)
      teachers = models.ForeignKey(Teachers, on_delete=models.SET_NULL,null=True)
      def __str__(self):
            return f"{self.subject} - {self.topic} on {self.date}"

