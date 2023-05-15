# models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# models.py
from django.contrib.auth.models import User
from django.db import models

# models.py
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username, name, password, email=None, **extra_fields):
        if not username:
            raise ValueError(_('Student Code must be set'))
        if not name:
            raise ValueError(_('Name must be set'))
        
        user = self.model(username=username, name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, name, password, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(username, name, password, email, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    flag = models.BooleanField()

    # Add related_name arguments to avoid clashes with auth.User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    # Set USERNAME_FIELD and REQUIRED_FIELDS as before
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.username
