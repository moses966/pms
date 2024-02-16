from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from hotel.models import Room
from management.models import BaseUserProfile

class HousekeepingTask(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    room_number = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='housekeeping_tasks', 
    )
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Room Maintenance Task'
        verbose_name_plural = 'Room Maintenance Tasks'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Call the method to handle CleanRoom removal
        self.handle_clean_room()

    def handle_clean_room(self):
        if self.task_status == 'pending':
            # Remove room from CleanRoom if present
            CleanRoom.objects.filter(room=self.room_number).delete()

    def __str__(self):
        return f"Task for Room {self.room_number} - {self.get_task_status_display()}"

class MaintenanceRequest(models.Model):
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Any important message that the manager or counter need to know.'
    )
    created_at = models.DateTimeField(default=timezone.now)
    assigned_to = models.ManyToManyField(
        BaseUserProfile,
        related_name='maintenance_tasks',
        blank=True,  # Allow the field to be left empty
    )
    resolved = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    housekeeping_task = models.OneToOneField(
        HousekeepingTask,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='maintenance_request',
    )
    def clean(self):
        # Ensure only one progress status is selected
        progress_count = sum([self.in_progress, self.resolved])
        if progress_count != 1:
            raise ValidationError("Select exactly one rate plan.")
    
    def save(self, *args, **kwargs):
        if self.resolved:
            self.housekeeping_task.task_status = 'completed'
            CleanRoom.objects.update_or_create(
                room=self.housekeeping_task.room_number,
                defaults={'last_cleaned': timezone.now()}
            )
        elif self.in_progress:
            self.housekeeping_task.task_status = 'in_progress'
            # Automatically remove room from CleanRoom if in progress
            CleanRoom.objects.filter(room=self.housekeeping_task.room_number).delete()
        self.housekeeping_task.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Check if there are any existing CleanRoom instances for the room
        existing_clean_room = CleanRoom.objects.filter(room=self.housekeeping_task.room_number).first()
        if existing_clean_room:
            # Delete the CleanRoom instance if it exists
            existing_clean_room.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Maintenance Request for Room {self.housekeeping_task.room_number}"
    
    class Meta:
        verbose_name = 'Maintenance Update'
        verbose_name_plural = 'Maintenance Updates'

class CleanRoom(models.Model):
    room = models.OneToOneField(
        Room,
        on_delete=models.CASCADE,
        related_name='clean_room',
    )
    last_cleaned = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Clean Room'
        verbose_name_plural = 'Clean Rooms'

    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is newly created
            # Check if there exists an associated HousekeepingTask instance
            associated_housekeeping_task = HousekeepingTask.objects.filter(room_number=self.room).first()
            if associated_housekeeping_task:
                # Delete the associated HousekeepingTask instance
                associated_housekeeping_task.delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Room {self.room.room_number} - Last cleaned: {self.last_cleaned}"
