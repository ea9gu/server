from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username, name, password, flag, email=None, **extra_fields):
        if not username:
            raise ValueError(_('Student Code must be set'))
        if not name:
            raise ValueError(_('Name must be set'))
        user = self.model(username=username, name=name, email=None, flag=flag, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, name, password, flag, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

class User(AbstractUser):
    username = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    flag = models.BooleanField()

    email = models.EmailField(_('email address'), blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'flag']

    objects = UserManager()

    def __str__(self):
        return self.username
