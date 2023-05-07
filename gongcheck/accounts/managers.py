from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    # def create_user(self, email, password, **extra_fields):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('Student Code must be set'))
        # if not email:
        #     raise ValueError(_('The Email must be set'))
        # email = self.normalize_email(email)
        # user = self.model(email=email, **extra_fields)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # def create_superuser(self, email, password, **extra_fields):
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)