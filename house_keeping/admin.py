from django.contrib import admin
from .models import HousekeepingTask, MaintenanceRequest, CleanRoom
from .forms import HousekeepingTaskForm

class MaintenanceRequestInline(admin.StackedInline):
    model = MaintenanceRequest
    extra = 0
    fields = ('description', 'assigned_to', 'in_progress','resolved', 'resolved_at')

@admin.register(HousekeepingTask)
class HousekeepingTaskAdmin(admin.ModelAdmin):
    form = HousekeepingTaskForm
    list_display = ('room_number', 'task_status', 'created_at', 'updated_at')
    list_filter = ('task_status',)
    search_fields = ('room_number__room_number',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('task_status',)
    inlines = [MaintenanceRequestInline]

@admin.register(CleanRoom)
class CleanRoomAdmin(admin.ModelAdmin):
    list_display = ('room', 'last_cleaned')
    search_fields = ('room__room_number',)
