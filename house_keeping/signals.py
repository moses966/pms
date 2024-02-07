from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import HousekeepingTask, CleanRoom, MaintenanceRequest
from django.utils import timezone

@receiver(pre_save, sender=HousekeepingTask)
def delete_previous_task(sender, instance, **kwargs):
    # Check if there's an existing HousekeepingTask for the same room
    previous_task = HousekeepingTask.objects.filter(room_number=instance.room_number).first()
    if previous_task:
        # Delete the previous task before saving the new one
        previous_task.delete()

@receiver(post_save, sender=MaintenanceRequest)
def add_room_to_clean_rooms(sender, instance, created, **kwargs):
    if instance.resolved:
        CleanRoom.objects.get_or_create(room=instance.housekeeping_task.room_number)

@receiver(post_save, sender=HousekeepingTask)
def remove_room_from_clean_rooms(sender, instance, created, **kwargs):
    CleanRoom.objects.filter(room=instance.room_number).delete()

@receiver(pre_delete, sender=HousekeepingTask)
def restore_room_to_clean_rooms(sender, instance, **kwargs):
    CleanRoom.objects.get_or_create(room=instance.room_number)