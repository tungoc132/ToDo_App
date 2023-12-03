from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

import datetime
from django.views import generic
from todo.form import BS4ScheduleForm, SimpleScheduleForm
from . import mixins

class Login(LoginView):
    template_name = 'auth/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('alltasks')

class RegisterView(FormView):
    template_name = 'auth/regist.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('alltasks')
    
    def form_valid(self, form):
       user = form.save()
       if user is not None:
           login(self.request, user)
       return super(RegisterView, self).form_valid(form)
   
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('alltasks')
        return super(RegisterView, self).get(*args, **kwargs)      

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

class MonthWithScheduleCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    template_name = 'base/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class MonthWithFormCalendar(mixins.MonthWithFormsMixin, generic.View):
    template_name = 'base/month_with_forms.html'
    model = Schedule
    date_field = 'date'
    form_class = SimpleScheduleForm

    def get(self, request, **kwargs):
        context = self.get_month_calendar()
        formset = context['month_formset']
        if formset.is_valid():
            formset.save()
            return redirect('month_with_forms')
        return render(request, self.template_name, context)


class MyCalendar(mixins.MonthCalendarMixin, mixins.WeekCalendarMixin, generic.CreateView):
    template_name = 'base/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect('mycalendar', year=date.year, month=date.month, day=date.day)
