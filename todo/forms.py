from django import forms
from .models import Profile, Task

from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget

class RegisterForm(UserCreationForm):    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name' , 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        
class TaskForm(forms.ModelForm):
    # title = forms.TextInput()
    # description = forms.TextInput()
    # complete = forms.BooleanField()
    date = forms.DateField(widget=AdminDateWidget())
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'date']
        # widgets = {
        #     "deadline": AdminDateWidget()
        # }