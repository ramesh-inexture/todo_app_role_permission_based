from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


# CUSTOM USER
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None, **KWARGS):
        """Creates and saves a User with the given email, first_name, last_name, user_name,
        date_of_birth and password."""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **KWARGS
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **KWARGS):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            **KWARGS
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    user_name = models.CharField(max_length=150, unique=True)
    profile_picture = models.ImageField(default='')
