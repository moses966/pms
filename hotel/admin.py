from django.contrib import admin
from .models import Room


class RoomAdmin(admin.ModelAdmin):
    fields = ('name','capacity','description')
    list_display = ['name', 'capacity']
    search_fields = ['name', 'capacity']

admin.site.register(Room, RoomAdmin)
