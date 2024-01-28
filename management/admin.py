from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, BaseUserProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm


class BaseUserProfileInline(admin.StackedInline):
    model = BaseUserProfile
    can_delete = False
    verbose_name = 'Personal Information'
    verbose_name_plural = 'Personal Information'
    fields = ('surname', 'given_name',
              'gender', 'contact', 'next_of_kin',
              'emergency_contact',
              'date_of_birth', 'place_of_birth', 'nin', 'age', 'location',
              )
    classes = ('collapse',)

class UserAdmin(BaseUserAdmin):
    inlines = (BaseUserProfileInline,)
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(User, UserAdmin)

admin.site.site_header = 'HM HOTEL'
admin.site.site_title = 'HM Hotel Administration'
admin.site.index_title = 'Welcome to HM Hotel Administration'