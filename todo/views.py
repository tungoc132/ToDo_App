from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from .models import Task
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# from django.contrib.admin.widgets import AdminSplitDateTime, AdminDateWidget, AdminTimeWidget


class Login(LoginView):
    template_name = 'auth/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('alltasks')  

def regist(request):
    if request.method == 'GET':
        form = RegisterForm()
        redirect_authenticated_user = True
        return render(request, 'auth/regist.html', {'form' : form})
    
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()
            # login(request, user)
            return redirect('login')
        else:
            return render(request, 'auth/regist.html', {'form': form})
        
@login_required
def userUpdate(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('alltasks')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'profile/profile_edit.html', context)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'alltasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alltasks'] = context['alltasks'].filter(user=self.request.user)
        context['count'] = context['alltasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        
        if search_input:
            context['alltasks'] = context['alltasks'].filter(
                title__icontains=search_input)
        context['search_input'] = search_input
        
        return context
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('alltasks')
    
    def form_valid(self, form):
       form.instance.user = self.request.user
       return super(TaskCreate, self).form_valid(form)

class TaskEdit(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('alltasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('alltasks')
    template_name = 'todo/confirm_delete.html'

# def deleteTask(request, pk):
#     deltask = get_object_or_404(Task, id=pk)
#     if request.method == 'post':
#         Task.delete()
#         messages.success(request, 'Task successfully deleted!')
#         return redirect('alltasks')
#     else:
#         return render(request, 'todo/confirm_delete.html', {'deltask': deltask})

# def edit_profile(request):
#     if request.method == 'POST':
#         form = UserChangeForm(request.POST, instance=request.user)
#         form.save(commit=False)
        
#         if form.is_valid():
#             usrname = form.cleaned_data['username']
#             fname = form.cleaned_data['first_name']
#             lname = form.cleaned_data['last_name']
#             email = form.cleaned_data['email']
#         return redirect('alltasks')
        
#     else:
#         form = UserChangeForm(instance=request.user)
#         context = {'form':form}
#         return render(request, 'profile/profile_edit.html', context)

        
