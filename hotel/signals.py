from django.dispatch import receiver
from django.utils import timezone


def update_room_cleaned(sender, instance, **kwargs):
    # Update the corresponding Room instance's cleaned field to 'Yes'
    instance.room.cleaned = 'Yes'
    instance.room.save()

def update_room_cleaned_on_delete(sender, instance, **kwargs):
    # Check if the corresponding Room instance exists
    if instance.room:
        # Update the cleaned field to 'Not yet' upon deletion of the CleanRoom instance
        instance.room.cleaned = 'Not yet'
        instance.room.save()
