from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('save_student/', views.save_student, name='save_student'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('list_files/', views.list_files, name='list_files'),
]

