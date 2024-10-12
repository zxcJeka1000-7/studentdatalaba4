from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'subject', 'grade']

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if grade < 0 or grade > 100:
            raise forms.ValidationError("Grade must be between 0 and 100.")
        return grade
