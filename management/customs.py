from django.contrib.auth.models import Group
from django.db import models

# model for departments
class Departments(Group):
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
