# app/forms.py
from django import forms
from django.core.exceptions import ValidationError

class StudentForm(forms.Form):
    name = forms.CharField(max_length=100, label='Имя')
    subject = forms.CharField(max_length=100, label='Предмет')
    grade = forms.IntegerField(label='Оценка')

    # Варианты формата файла
    file_format = forms.ChoiceField(choices=[('json', 'JSON'), ('xml', 'XML')], label='Формат файла')

    # Переопределяем метод для валидации
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.strip():  # Проверяем, чтобы имя не было пустым
            raise ValidationError('Имя не должно быть пустым.')
        return name

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        if not subject.strip():  # Проверяем, чтобы предмет не был пустым
            raise ValidationError('Предмет не должен быть пустым.')
        return subject

    def clean_grade(self):
        grade = self.cleaned_data['grade']
        if grade < 0 or grade > 100:  # Проверяем диапазон оценки
            raise ValidationError('Оценка должна быть в диапазоне от 0 до 100.')
        return grade
