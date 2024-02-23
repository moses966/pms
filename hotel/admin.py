from django.contrib import admin
from django.utils import timezone
from .models import Room, Category, Guest, Booking, Reservation, PaymentInformation
from house_keeping.models import CleanRoom

# adding Category to admin
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'count', 'capacity', 'price', 'description',)
    list_display = ('name', 'price', 'capacity', 'created_at', 'updated_at')
    search_fields = ('name', 'capacity')
    list_filter = ('capacity',)


# Adding Rooms model to admin
class RoomAdmin(admin.ModelAdmin):
    fields = ('name','room_number', 'floor_number',
              'capacity', 'standard_price', 'promotional_price', 'corporate_price', 'discount', 'category', 'description', 'status',)
    list_display = ['name', 'cleaned', 'capacity', 'room_number',
         'standard_price', 'corporate_price', 'status', 'check_in_date_for_reservations', 'get_last_cleaned']
    search_fields = ['name', 'capacity', 'status']
    list_filter = ('status', 'floor_number',)
    readonly_fields = ('promotional_price',)
    def check_in_date_for_reservations(self, obj):
        # Get the check-in date for reservations associated with this room
        reservations_check_in_dates = [reservation.check_in_date for reservation in obj.reservations.all()]
        # Return the earliest check-in date
        return min(reservations_check_in_dates, default=None)
    
    check_in_date_for_reservations.short_description = 'Earliest Check-in Date'

    def get_last_cleaned(self, obj):
        """
        Custom method to display the last cleaned time for the room.
        """
        try:
            # Get the CleanRoom instance for the room
            clean_room = CleanRoom.objects.get(room=obj)
            # Return the last_cleaned time if available
            return clean_room.last_cleaned.strftime('%Y-%m-%d %H:%M:%S') if clean_room.last_cleaned else "Not Sure!"
        except CleanRoom.DoesNotExist:
            return "Not Sure!"

    get_last_cleaned.short_description = 'Last Cleaned'

# adding PaymentInformation model to admin
class PaymentInformationInline(admin.StackedInline):
    model = PaymentInformation
    can_delete = False
    verbose_name = 'Payment Details'
    verbose_name_plural = 'Payment Details'
    classes = ('collapse',)
    extra = 0
    readonly_fields = ('amount_paid',)
    fields = (
        'payment_status','payment_method', 'standard_rate','promotional_rate',
        'corporate_rate', 'amount_paid',
    )

# adding Reservation to admin
class ReservationAdmin(admin.ModelAdmin):
    fields = ('guest_name', 'guest_email', 'guest_contact', 'number_of_children', 'number_of_adults',
              'room_or_rooms', 'reservation_date', 'check_in_date', 'check_out_date', 'deadline', 'check_in', 'special_requests', 'created_at', 'status',
              'deposit', 'deposit_amount', 'balance'
    )
    list_display = ('guest_name', 'guest_contact', 'deposit',
        'get_room_numbers', 'get_amount_paid', 'status', 'reservation_number', 'check_in',
    )
    search_fields = ('guest_name', 'guest_contact', 'guest_email', 'status', 'reservation_number',)
    list_filter = ('room_or_rooms', 'status',)
    readonly_fields = ['created_at']
    inlines = [
        PaymentInformationInline,
    ]

    def get_room_numbers(self, obj):
        room_numbers = ", ".join(room.room_number for room in obj.room_or_rooms.all())
        return room_numbers if room_numbers else "No rooms booked"
    get_room_numbers.short_description = 'Room Number'

    def get_amount_paid(self, obj):
        """
        Method to retrieve the amount paid for each reservation.
        """
        # Assuming PaymentInformation is related to Reservation via a ForeignKey named 'reserve_info'
        payment_info = obj.reserve_info.first()
        if payment_info:
            return payment_info.amount_paid
        return None  # Return None if no payment information is available

    get_amount_paid.short_description = 'Amount Paid'  # Customize column header

class GuestInline(admin.StackedInline):
    model = Guest
    classes = ('collapse',)
    can_delete = False
    extra = 1
    fields = ('full_name', 'gender', 'email_adress', 'phone_number', 'nin', 'address')

# adding Booking model to admin
class BookingAdmin(admin.ModelAdmin):
    verbose_name = 'Booking Details'
    verbose_name_plural = 'Booking Details'
    readonly_fields = ('booking_number',)
    search_fields = ('booking_date', 'booking_number',)
    fields = (
        'children','number_of_children', 'number_of_adults','room_or_rooms','booking_date','check_in_date','check_out_date',
        'booking_status', 'check_in', 'booking_source','special_requests',
        'special_instructions','booking_number',
    )
    inlines = (
        GuestInline,
        PaymentInformationInline,
    )
    list_filter = [
        'room_or_rooms', 'booking_status',
    ]
    # Define list display with desired fields
    list_display = ('get_guest_full_name', 'get_guest_phone_number',
        'get_room_number', 'booking_number', 'booking_status', 'check_in', 'get_amount_paid',
    )

    # Optionally, include these methods directly in the list display
    def get_guest_full_name(self, obj):
        return obj.guest_profile.full_name if obj.guest_profile else None

    def get_guest_phone_number(self, obj):
        return obj.guest_profile.phone_number if obj.guest_profile else None

    def get_room_number(self, obj):
        room_numbers = ", ".join(room.room_number for room in obj.room_or_rooms.all())
        return room_numbers if room_numbers else None
    
    def get_amount_paid(self, obj):
        # Assuming PaymentInformation is related to Booking via a ForeignKey named 'booking_info'
        payment_info = obj.booking_info.first()
        if payment_info:
            return payment_info.amount_paid
        return None  # Return None if no payment information is available

    # Customize column headers if needed
    get_guest_full_name.short_description = 'Guest Full Name'
    get_guest_phone_number.short_description = 'Guest Phone Number'
    get_room_number.short_description = 'Room Number'
    get_amount_paid.short_description = 'Amount Paid'

# registering models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Booking, BookingAdmin)
