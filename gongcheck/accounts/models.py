# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils.translation import gettext_lazy as _

# from .managers import UserManager

# class User(AbstractUser):
#     # username = None
#     # email = models.EmailField(_('email address'), unique=True)
#     username = models.CharField(max_length=10, unique=True)
#     email = None

#     # USERNAME_FIELD = 'email'
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []

#     objects = UserManager()

#     def __str__(self):
#         return self.username

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=10, unique=True)

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
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
