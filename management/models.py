from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .managers import CustomUserManager
from .customs import Departments, Equipment
from .custom_validators import validate_nin, validate_contact

# model for creation of user
class User(AbstractBaseUser, PermissionsMixin):

    Positions = [
        ('man', 'Manager'),
        ('hum', 'Human Resource'),
        ('cou', 'Counter'),
        ('pub', 'Officer public relations'),
        ('rom', 'Room attendant'),
    ]
    
    email = models.EmailField(
        _("email address"),
        unique=True,
        validators=[EmailValidator(message="Invalid email address")],
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    position = models.CharField(
        max_length=30,
        choices=Positions,
        default="man",
        null=False,
        blank=False,
        help_text="Choose User Position in the hotel management",
    )
   
    

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
        null=False, 
        blank=False,
        default='male',
        help_text="Choose Gender"
    )

    contact = models.CharField(
        max_length=10,
        validators=[validate_contact],
    )
    location = models.TextField(max_length=120)
    next_of_kin = models.CharField(max_length=30)
    emergency_contact = models.CharField(
        max_length=10,
        validators=[validate_contact],
        help_text='Contact to your next of kin',
    )
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='images/', null=True, blank=True)
    place_of_birth = models.CharField(max_length=20)
    age = models.IntegerField()
    nin = models.CharField(
        max_length=24,
        verbose_name='NIN',
        help_text='National Identification number',
        validators=[validate_nin],
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"{self.surname} {self.given_name}"



# miscellaneous model
class Miscellaneous(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='miscella',
    )
    salary = models.FloatField(
        max_length=17,
        null=True,
        blank=True,
        help_text='Input only the UGX amount e.g: 50000',
    )
    payment = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        help_text='If applicable, provide bank account/airtel pay code/MOMO pay code.',
        verbose_name='Payment Details'
    )
    userid = models.CharField(
        max_length=2,
        null=False, 
        blank=False,
        help_text="Enter user ID number(01-99).",
        verbose_name='Personal ID',
    )

    ackno = models.BooleanField(
        default=False,
        verbose_name='Acknowledgement of company rules and procedures.',
        help_text='Ask user if they consent to company policies and procedures.'
    )
    def __str__(self):
        return f"Miscellaneous info for {self.user.email}"

# class to allocate equipments
class EquipmentAllocation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='equipment_allocations',
    )
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='allocations',
    )
    quantity_allocated = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity_allocated} {self.equipment.name} allocated to {self.user.email}"

# model to customize the group model
class CustomGroup(models.Model):
    group = models.OneToOneField(
        Departments,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    leader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='department_leader',
    )

    def __str__(self):
        return self.group.name
    
# User employment information
class EmploymentInformation(models.Model):
    EMPLOY = [
        ('ft', 'full-time'),
        ('pt', 'part-time'),
        ('ct', 'contract'),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employment_info',
    )
    employment_status = models.CharField(
        max_length=15,
        choices=EMPLOY,
        null=False, 
        blank=False,
        default='ft',
        help_text="Choose Status"
    )
    department = models.ForeignKey(
        Departments,
        on_delete=models.CASCADE,
    )
    employment_start_date = models.DateField()
    head_of_department = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='department_head_positions',
        limit_choices_to={'department_leader__isnull': False},
        help_text="Choose Department Head"
    )
    def __str__(self):
        return f"{self.employment_status} employment in {self.department} department"