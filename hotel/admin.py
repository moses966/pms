from django.contrib import admin
from .models import Room, Category

class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'count', 'capacity', 'price', 'description',)
    list_display = ('name', 'price', 'capacity', 'created_at', 'updated_at')
    search_fields = ('name', 'capacity')
    list_filter = ('capacity',)


class RoomAdmin(admin.ModelAdmin):
    fields = ('name','room_number', 'floor_number',
              'capacity', 'price', 'category', 'description', 'status',)
    list_display = ['name', 'capacity', 'price', 'status']
    search_fields = ['name', 'capacity', 'status']
    list_filter = ('status',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Room, RoomAdmin)
