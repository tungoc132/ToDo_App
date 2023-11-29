from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskEdit, TaskDelete, Login, RegisterView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page = 'login'), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    
    path('', TaskList.as_view(), name='alltasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('create-task', TaskCreate.as_view(), name='create-task'),
    path('task-edit/<int:pk>/', TaskEdit.as_view(), name='task-edit'),
    path('deletetask/<int:pk>/', TaskDelete.as_view(), name='deletetask'),
]