from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskEdit, Login
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page = 'login'), name='logout'),
    path('register', views.regist, name='register'),
    
    path('', TaskList.as_view(), name='alltasks'),
    
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('create-task', TaskCreate.as_view(), name='create-task'),
    path('task-edit/<int:pk>/', TaskEdit.as_view(), name='task-edit'),
    path('deletetask/<int:pk>/', views.TaskDelete.as_view(), name='deletetask'),
    # path('deltask/<int:pk>/', views.deleteTask, name="deltask"),
    path('profile-edit', views.userUpdate, name='profile-edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)