from django.contrib import admin
from .models import Events

@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'mobile_contact', 'service', 'reservation_date',
        'number_of_days', 'number_of_guests', 'sub_total_amount'
    ]