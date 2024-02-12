# In your tasks.py file

from celery import shared_task
from django.utils import timezone
from .models import Remove, PileUp

@shared_task
def subtract_one_periodically():
    # Retrieve the instance of Remove from the database
    remove_instance = Remove.objects.first()

    if remove_instance:
        # Subtract 1 from the number field
        remove_instance.number -= 1
        remove_instance.save()

@shared_task(name='Add_one_to_number')
def add_one_periodically():
    # Retrieve the instance of Remove from the database
    add_instance = PileUp.objects.first()

    if add_instance:
        # Subtract 1 from the number field
        add_instance.number += 1
        add_instance.save()
