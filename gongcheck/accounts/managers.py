from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username, password, name, email, flag, **extra_fields):
        if not username:
            raise ValueError(_('Student Code must be set'))
        user = self.model(username=username, name=name, email=email, flag=flag, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, name, email, flag, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, name, email, flag, **extra_fields)
