# app/urls.py
from django.urls import path
from .views import (
    index,
    save_student,
    upload_file,
    list_files,
    view_file,
    student_list,
    import_to_db,
    delete_student,
    delete_file,  # Убедитесь, что запятая здесь корректна
)


urlpatterns = [
    path('', index, name='index'),
    path('save_student/', save_student, name='save_student'),
    path('upload_file/', upload_file, name='upload_file'),
    path('list_files/', list_files, name='list_files'),
    path('files/view/<str:file_name>/', view_file, name='view_file'),
    path('import_to_db/<str:file_name>/', import_to_db, name='import_to_db'),
    path('students/', student_list, name='student_list'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student'),
    path('delete_file/<str:file_name>/', delete_file, name='delete_file'),# Используем просто student_list, т.к. функция уже импортирована
]

