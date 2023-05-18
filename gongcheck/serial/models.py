from django.db import models

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=10)
    device_name = models.CharField(max_length=100)
    device_serial = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)