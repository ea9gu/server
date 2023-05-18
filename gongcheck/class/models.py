from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    course_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    professor_id = models.CharField(max_length=10) # 교수의 ID를 저장

    def __str__(self):
        return self.name

class StudentCourse(models.Model):
    student_id = models.IntegerField()  # 학생의 ID를 저장
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student_id} - {self.course}'