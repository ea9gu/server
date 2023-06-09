from django.db import models
from django.utils import timezone

class AudioFile(models.Model):
    # 교수가 생성한 주파수 정보
    frequency = models.IntegerField()
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    course_id = models.CharField(max_length=100, unique=False)
    number = models.IntegerField()
    activation_duration = models.IntegerField()
    def get_file_url(self):
        return self.file_path

class Attendance(models.Model):
    # 학생의 녹음 음성 파일 정보
    attendance_id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=100)
    course_id = models.CharField(max_length=100, unique=False)
    date = models.DateField()
    attend = models.BooleanField()
    course_number = models.IntegerField()
