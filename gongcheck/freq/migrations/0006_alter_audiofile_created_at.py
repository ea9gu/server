# Generated by Django 3.2.4 on 2023-05-25 16:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('freq', '0005_auto_20230524_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
