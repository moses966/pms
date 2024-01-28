from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .managers import CustomUserManager

# model for creation of user
class User(AbstractBaseUser, PermissionsMixin):

    Positions = [
        ('man', 'Manager'),
        ('hum', 'Human Resource'),
        ('cou', 'Counter'),
        ('pub', 'Officer public relations'),
        ('rom', 'Room attendant'),
    ]
    
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    position = models.CharField(
        max_length=30, choices=Positions, default="-----", 
        null=True, blank=True, help_text="Choose User Position in the hotel management")
   
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

User = get_user_model()

# Personal Information model
class BaseUserProfile(models.Model):
    gender_s = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        )
    surname = models.CharField(max_length=17)
    given_name = models.CharField(max_length=15)
    gender = models.CharField(
        max_length=10,
        choices=gender_s,
        null=True, 
        blank=True,
        default='-----',
        help_text="Choose Gender"
        )

    contact = models.CharField(max_length=15)
    location = models.TextField(max_length=120)
    next_of_kin = models.CharField(max_length=30)
    emergency_contact = models.CharField(
        max_length=15,
        help_text='Contact to your next of kin',
        )
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=20)
    age = models.IntegerField()
    nin = models.CharField(
        max_length=24,
        verbose_name='NIN',
        help_text='National Identification number',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.surname} {self.given_name}"

# model to customize the group model
class CustomGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='leading_groups')

    def __str__(self):
        return self.group.name