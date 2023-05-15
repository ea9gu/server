from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class Student(AbstractUser):
    username = models.CharField(max_length=10, unique=True, verbose_name='학번')
    name = models.CharField(max_length=255, verbose_name='이름')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='student_set',
        blank=True,
        help_text='The groups this student belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='student_set',
        blank=True,
        help_text='Specific permissions for this student.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '학생'
        verbose_name_plural = '학생'


class Professor(AbstractUser):
    username = models.CharField(max_length=10, unique=True, verbose_name='교번')
    name = models.CharField(max_length=255, verbose_name='이름')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='professor_set',
        blank=True,
        help_text='The groups this professor belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='professor_set',
        blank=True,
        help_text='Specific permissions for this professor.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '교수'
        verbose_name_plural = '교수'
