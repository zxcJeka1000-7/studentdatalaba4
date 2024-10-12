# app/views.py
import json
import os
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import StudentForm
from .models import Student
from django.shortcuts import get_object_or_404, redirect

def index(request):
    return render(request, 'index.html')
def save_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            grade = form.cleaned_data['grade']
            file_format = form.cleaned_data['file_format']

            print(f"Полученные данные: {name}, {subject}, {grade}, {file_format}")  # Отладочная информация


            # Формируем данные для сохранения
            student_data = {
                'name': name,
                'subject': subject,
                'grade': grade
            }

            if file_format == 'json':
                file_name = f"{name}_data.json"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(student_data, json_file, ensure_ascii=False, indent=4)
            elif file_format == 'xml':
                file_name = f"{name}_data.xml"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                root = ET.Element('student')  # Создание корневого элемента
                ET.SubElement(root, 'name').text = name
                ET.SubElement(root, 'subject').text = subject
                ET.SubElement(root, 'grade').text = str(grade)  # Преобразование grade в строку
                tree = ET.ElementTree(root)
                tree.write(file_path, encoding='utf-8', xml_declaration=True)

                print(f"Сохранен XML файл: {file_path}")  # Отладочная информация
                print(f"Содержимое файла: {ET.tostring(root, encoding='unicode')}")  # Отладка содержимого

            return redirect('list_files')  # Перенаправляем на страницу с файлами

    else:
        form = StudentForm()

    return render(request, 'save_student.html', {'form': form})

def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.json') or uploaded_file.name.endswith('.xml'):
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            return redirect('list_files')
        else:
            # Выводим сообщение об ошибке
            return render(request, 'upload_file.html', {'error': 'Недопустимый формат файла. Пожалуйста, загрузите JSON или XML файл.'})

    return render(request, 'upload_file.html')

def list_files(request):
    media_path = os.path.join(settings.MEDIA_ROOT)
    json_files = [f for f in os.listdir(media_path) if f.endswith('.json')]
    xml_files = [f for f in os.listdir(media_path) if f.endswith('.xml')]
    
    return render(request, 'list_files.html', {
        'json_files': json_files,
        'xml_files': xml_files,
    })

def view_file(request, file_name):
    media_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if file_name.endswith('.json'):
        with open(media_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Проверка структуры данных
            if isinstance(data, dict):  # Если данные представлены в виде одного студента
                name = data.get('name', 'Неизвестно')
                subject = data.get('subject', 'Неизвестно')
                grade = data.get('grade', 0)
                Student.objects.create(name=name, subject=subject, grade=grade)

                return render(request, 'view_file.html', {'data': data, 'file_name': file_name})

            elif 'students' in data:  # Если данные представлены как список студентов
                for item in data['students']:
                    name = item.get('name', 'Неизвестно')
                    subject = item.get('subject', 'Неизвестно')
                    grade = item.get('grade', 0)
                    Student.objects.create(name=name, subject=subject, grade=grade)

                return render(request, 'view_file.html', {'data': data, 'file_name': file_name})

            else:
                return HttpResponse("Неверный формат JSON", status=400)

    elif file_name.endswith('.xml'):
        tree = ET.parse(media_path)
        root = tree.getroot()

        for student in root.findall('student'):
            name = student.find('name').text
            subject = student.find('subject').text
            grade = student.find('grade').text
            Student.objects.create(name=name, subject=subject, grade=float(grade))  # Преобразуем grade в float

        data = ET.tostring(root, encoding='utf-8').decode('utf-8')
        return render(request, 'view_file.html', {'data': data, 'file_name': file_name})

    return HttpResponse("Файл не найден", status=404)

def student_list(request):
    students = Student.objects.all()  # Извлекаем всех студентов из базы
    return render(request, 'student_list.html', {'students': students})



def import_to_db(request, file_name):
    print(f"Импортируем файл: {file_name}")  # Отладочный вывод

    media_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # Если файл JSON
    if file_name.endswith('.json'):
        with open(media_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if isinstance(data, dict):  # Если это один студент
                name = data.get('name', 'Неизвестно')
                subject = data.get('subject', 'Неизвестно')
                grade = data.get('grade', 0)
                Student.objects.create(name=name, subject=subject, grade=grade)

            elif 'students' in data:  # Если это список студентов
                for student in data['students']:
                    name = student.get('name', 'Неизвестно')
                    subject = student.get('subject', 'Неизвестно')
                    grade = student.get('grade', 0)
                    Student.objects.create(name=name, subject=subject, grade=grade)

    # Если файл XML
    elif file_name.endswith('.xml'):
        tree = ET.parse(media_path)
        root = tree.getroot()

        for student in root.findall('student'):
            name = student.find('name').text
            subject = student.find('subject').text
            grade = student.find('grade').text
            Student.objects.create(name=name, subject=subject, grade=float(grade))

    return redirect('list_files')  # Возвращаемся к списку файлов после импорта



def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')  # Перенаправление на страницу списка студентов




def delete_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)  # Путь к файлу

    if os.path.isfile(file_path):  # Проверяем, существует ли файл
        os.remove(file_path)  # Удаляем файл
    else:
        return HttpResponse("Файл не найден.", status=404)

    return redirect('list_files')  # Перенаправляем на страницу со списком файлов
