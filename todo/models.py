from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# model for database
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    # Set the order base on "complete" value
    class Meta:
        ordering = ['complete']

class Schedule(models.Model):
    summary = models.CharField('summary', max_length=50)
    description = models.TextField('description', blank=True)
    start_time = models.TimeField('start time', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('end time', default=datetime.time(7, 0, 0))
    date = models.DateField('date')
    created_at = models.DateTimeField('created at', default=timezone.now)
    def __str__(self):
        return self.summary

