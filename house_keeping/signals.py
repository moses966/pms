from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import HousekeepingTask

@receiver(pre_save, sender=HousekeepingTask)
def delete_previous_task(sender, instance, **kwargs):
    # Check if there's an existing HousekeepingTask for the same room
    previous_task = HousekeepingTask.objects.filter(room_number=instance.room_number).first()
    if previous_task:
        # Delete the previous task before saving the new one
        previous_task.delete()