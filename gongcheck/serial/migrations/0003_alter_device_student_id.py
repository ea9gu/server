# Generated by Django 3.2.4 on 2023-05-16 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serial', '0002_device_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='student_id',
            field=models.CharField(max_length=10),
        ),
    ]
