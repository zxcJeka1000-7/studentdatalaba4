import os
import json
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student
from .forms import StudentForm

def index(request):
    return render(request, 'index.html')  # Главная страница приложения

def save_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем данные в базе данных
            return redirect('index')  # Перенаправляем на главную страницу
    else:
        form = StudentForm()  # Создаем пустую форму для отображения
    return render(request, 'save_student.html', {'form': form})

def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        # Обработка загрузки JSON файла
        if uploaded_file.name.endswith('.json'):
            try:
                data = json.load(uploaded_file)
                for item in data:
                    Student.objects.create(**item)  # Создаем объекты Student из JSON
                return HttpResponse("File uploaded and data saved successfully.")
            except json.JSONDecodeError:
                return HttpResponse("Invalid JSON file.")
        # Обработка загрузки XML файла
        elif uploaded_file.name.endswith('.xml'):
            try:
                tree = ET.parse(uploaded_file)
                root = tree.getroot()
                for student in root.findall('student'):
                    name = student.find('name').text
                    subject = student.find('subject').text
                    grade = float(student.find('grade').text)
                    Student.objects.create(name=name, subject=subject, grade=grade)
                return HttpResponse("File uploaded and data saved successfully.")
            except ET.ParseError:
                return HttpResponse("Invalid XML file.")
        else:
            return HttpResponse("File type not supported.")  # Поддерживаются только JSON и XML
    return render(request, 'upload_file.html')

def list_files(request):
    json_files = [f for f in os.listdir('uploads') if f.endswith('.json')]  # Получаем список JSON файлов
    xml_files = [f for f in os.listdir('uploads') if f.endswith('.xml')]  # Получаем список XML файлов
    return render(request, 'list_files.html', {'json_files': json_files, 'xml_files': xml_files})
