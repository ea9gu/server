from django.db import models

class AudioFile(models.Model):
    frequency = models.IntegerField()
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    course_id = models.IntegerField()
    number = models.IntegerField()

    def get_file_url(self):
        return self.file_path