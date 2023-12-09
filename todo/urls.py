from . import views
from .views import TaskList, TaskEdit, Login

from django.urls import path
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static

from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page = 'login'), name='logout'),
    path('register', views.regist, name='register'),
    
    path('', TaskList.as_view(), name='alltasks'),
    path('create-task', views.taskcreate, name='create-task'),
    path('task-edit/<int:pk>/', TaskEdit.as_view(), name='task-edit'),
    path('deletetask/<int:pk>/', views.TaskDelete.as_view(), name='deletetask'),
    path('profile-edit', views.userUpdate, name='profile-edit'),
    
    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)