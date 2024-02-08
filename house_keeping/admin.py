from django.contrib import admin
from .models import HousekeepingTask, MaintenanceRequest, CleanRoom

class MaintenanceRequestInline(admin.StackedInline):
    model = MaintenanceRequest
    extra = 0
    fields = ('assigned_to', 'description', 'in_progress', 'resolved', 'resolved_at')

@admin.register(HousekeepingTask)
class HousekeepingTaskAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'task_status', 'created_at', 'updated_at', 'person_responsible')
    list_filter = ('task_status',)
    search_fields = ('room_number__room_number',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('task_status',)
    inlines = [MaintenanceRequestInline]

    def person_responsible(self, obj):
        assigned_users = obj.maintenance_request.assigned_to.all()
        return ", ".join([f"{user.surname} {user.given_name}" for user in assigned_users])

@admin.register(CleanRoom)
class CleanRoomAdmin(admin.ModelAdmin):
    list_display = ('room', 'last_cleaned')
    search_fields = ('room__room_number', 'room__floor_number', 'room__status',)
    # Note: Search by room number, floor number, or status (available, occupied, out of service)
