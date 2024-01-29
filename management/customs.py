from django.contrib.auth.models import Group
from django.db import models

# model for departments
class Departments(Group):
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"


# model for handling 
class Equipment(models.Model):
    name = models.CharField(
        max_length=40,
    )
    total_number = models.IntegerField(
        default=0,
    )

    def __str__(self):
        return self.name