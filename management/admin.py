from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from .customs import Equipment
from .models import (
    User, 
    BaseUserProfile,
    CustomGroup,
    EmploymentInformation,
    Miscellaneous,
    EquipmentAllocation,
    )
from .forms import (
    CustomUserCreationForm, 
    CustomUserChangeForm,
    )
from .customs import Departments

# adding profile form to admin
class BaseUserProfileInline(admin.StackedInline):
    model = BaseUserProfile
    can_delete = False
    verbose_name = 'Personal Information'
    verbose_name_plural = 'Personal Information'
    fields = ('surname', 'given_name',
              'gender', 'contact', 'next_of_kin',
              'emergency_contact',
              'date_of_birth', 'place_of_birth', 'nin', 'age', 'location', 'photo',
              )
    classes = ('collapse',)

# adding employment form to admin
class EmploymentInformationInline(admin.StackedInline):
    model = EmploymentInformation
    fk_name = 'user'
    can_delete = False
    verbose_name = 'Employment Information'
    verbose_name_plural = 'Employment Information'
    fields = (
        'head_of_department',
        'employment_status',
        'employment_start_date',
    )
    classes = ('collapse',)


# adding miscell.. form to admin
class MiscellaneousInline(admin.StackedInline):
    model = Miscellaneous
    can_delete = False
    verbose_name = 'Other Requirements'
    verbose_name_plural = 'Other Requirements'
    fields = ('userid', 'payment',
              'salary', 'ackno',
              )
    classes = ('collapse',)

# adding equipments form to admin
class EquipmentAllocationInline(admin.TabularInline):
    model = EquipmentAllocation
    extra = 1  
    fields = [
        'equipment',
        'quantity_allocated',
        ]
    classes = ('collapse',)
    

class UserAdmin(BaseUserAdmin):
    inlines = (
        BaseUserProfileInline,
        EmploymentInformationInline,
        MiscellaneousInline,
        EquipmentAllocationInline,
        )
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


# customized group
class CustomGroupInline(admin.StackedInline):
    model = CustomGroup
    can_delete = False
    verbose_name = 'Department Head'
    verbose_name_plural = 'Department Heads'
    
# add the CustomGroup wiget to the admin interface
class CustomGroupAdmin(GroupAdmin):
    inlines = (CustomGroupInline,)

#adding the custom Equipment model to admin
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'total_number',
        ]

#register custom User in the admin
admin.site.register(User, UserAdmin)

#unregister default and register custom group
admin.site.unregister(Group)
admin.site.register(Departments, CustomGroupAdmin)

admin.site.site_header = 'HM HOTEL'
admin.site.site_title = 'HM Hotel Administration'
admin.site.index_title = 'Welcome to HM Hotel Administration'