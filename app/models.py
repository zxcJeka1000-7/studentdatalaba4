from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    grade = models.FloatField()

    def __str__(self):
        return f'{self.name} - {self.subject}: {self.grade}'