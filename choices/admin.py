from django.contrib import admin
from .models import (
    Positions, RoomStatus, BookingSource,
    BookingStatus, GenderChoices,
    PaymentStatus, PaymentMethod, EmploymentStatus,
    EmployPaymentMethod, MenuAndDrinksChoice, ServiceChoices, Additionals,
)

@admin.register(Positions)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ['position']

@admin.register(RoomStatus)
class RoomStatusAdmin(admin.ModelAdmin):
    list_display = ['room_status']

@admin.register(BookingSource)
class BookingSourceAdmin(admin.ModelAdmin):
    list_display = ['booking_source']

@admin.register(BookingStatus)
class BookingStatusAdmin(admin.ModelAdmin):
    list_display = ['booking_status']

@admin.register(GenderChoices)
class GenderChoicesAdmin(admin.ModelAdmin):
    list_display = ['gender_choices']

@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ['payment_status']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['payment_method']

@admin.register(EmploymentStatus)
class EmploymentStatusAdmin(admin.ModelAdmin):
    list_display = ['employment_status']

@admin.register(EmployPaymentMethod)
class EmployPayMethodAdmin(admin.ModelAdmin):
    list_display = ['payment_method']

@admin.register(MenuAndDrinksChoice)
class MenuAndDrinksChoiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'units', 'unit_price']

@admin.register(ServiceChoices)
class ServiceChoicesAdmin(admin.ModelAdmin):
    list_display = ['place', 'price_per_day']

@admin.register(Additionals)
class AdditionalsAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit_price']
