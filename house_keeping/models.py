from django.db import models
from django.utils import timezone
from management.models import CustomGroup, BaseUserProfile
from hotel.models import Room
from django.contrib.auth import get_user_model

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

    def __str__(self):
        return f"Task for Room {self.room_number} - {self.get_task_status_display()}"

class MaintenanceRequest(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='room_maintenance_requests', 
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Any important message that the manager or counter need to know.'
    )
    created_at = models.DateTimeField(default=timezone.now)
    assigned_to = models.ManyToManyField(
        BaseUserProfile,
        related_name='housekeeping_tasks',
        blank=True,  # Allow the field to be left empty
    )
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    housekeeping_task = models.OneToOneField(
        HousekeepingTask,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='maintenance_request',
    )

    def save(self, *args, **kwargs):
        # Update HousekeepingTask status based on MaintenanceRequest status
        if self.resolved:
            self.housekeeping_task.task_status = 'completed'
        elif self.resolved_at:
            self.housekeeping_task.task_status = 'in_progress'
        else:
            self.housekeeping_task.task_status = 'pending'
        self.housekeeping_task.save()  # Save the updated status
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Maintenance Request for Room {self.room.room_number}"

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

    def __str__(self):
        return f"Room {self.room.room_number} - Last cleaned: {self.last_cleaned}"
