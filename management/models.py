from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):

    Positions = [
        ('man', 'Manager'),
        ('hum', 'Human Resource'),
        ('cou', 'Counter'),
        ('pub', 'Officer public relations'),
        ('rom', 'Room attendant'),
    ]
    gender_s = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    position = models.CharField(
        max_length=30, choices=Positions, default="-----", 
        null=True, blank=True, help_text="Choose User Position in the hotel management")
    gender = models.CharField(
        max_length=10, choices=gender_s, null=True, 
        blank=True, default='-----', help_text="Choose Gender")
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

