from django.db import models
from django.contrib.auth.models import (PermissionsMixin, AbstractUser)
from .managers import CustomUserManager


# CUSTOM USER
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(
#         verbose_name='email',
#         max_length=255,
#         unique=True,
#     )
#     first_name = models.CharField(max_length=250, blank=True)
#     last_name = models.CharField(max_length=250, blank=True)
#     user_name = models.CharField(max_length=150, unique=True)
#     profile_picture = models.ImageField(default='default.jpeg', upload_to='profile_picture')
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return f"{self.id} | {self.email}"
#

class UserRoles(models.Model):
    role = models.CharField(max_length=200)


class User(AbstractUser):
    email = models.EmailField(
            verbose_name='email',
            max_length=255,
            unique=True,
        )
    profile_picture = models.ImageField(default='default.jpeg', upload_to='profile_picture')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.id} | {self.email}"

