from django.db import models

# Create your models here.
class Account(models.Model):
    student_id=models.CharField(max_length=7)
    password=models.CharField(max_length=12)
    name=models.CharField(max_length=10)