from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone

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
    time_of_allocation = models.DateTimeField(default=timezone.now, editable=False)
    def save(self, *args, **kwargs):
        if not self.pk:  # Only set timestamp if the object is being created, not updated
            self.time_of_allocation = timezone.now()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name