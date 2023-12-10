from django.db import models
from django.contrib.auth.models import User
import datetime

# model for database
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    date = models.DateField(default=datetime.date.today(), null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    # Set the order base on "complete" value
    class Meta:
        ordering = ['complete', 'date']
        
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'