from django.urls import path
from .views import register, login, logout,task_list,add_task,edit_task, delete_task

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('task_list', task_list, name='task_list'),
    path('add_task/', add_task, name='add_task'),
    path('edit_task/<str:task_id>/', edit_task, name='edit_task'),
    path('delete_task/<str:task_id>/', delete_task, name='delete_task'),
]
