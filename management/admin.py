from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['email']  # Use 'email' instead of 'username'
    list_display = ['email', 'is_staff', 'is_active']

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)