from django.contrib import admin
from .models import Room, Category, Booking, Guest, Reservation

# adding Category to admin
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'count', 'capacity', 'price', 'description',)
    list_display = ('name', 'price', 'capacity', 'created_at', 'updated_at')
    search_fields = ('name', 'capacity')
    list_filter = ('capacity',)

# adding Reservation to admin
class ReservationAdmin(admin.ModelAdmin):
    fields = ('guest_name', 'guest_email', 'guest_contact', 'number_of_children', 'number_of_adults',
              'room_or_rooms', 'check_in_date', 'check_out_date', 'special_requests', 'created_at',
              'deposit', 'deposit_amount',
    )
    list_display = ('guest_name', 'guest_contact', 'guest_email',)
    search_fields = ('guest_name', 'guest_contact', 'guest_email')
    list_filter = ('guest_name', 'room_or_rooms')

# Adding Rooms model to admin
class RoomAdmin(admin.ModelAdmin):
    fields = ('name','room_number', 'floor_number',
              'capacity', 'price', 'category', 'description', 'status',)
    list_display = ['name', 'capacity', 'price', 'status']
    search_fields = ['name', 'capacity', 'status']
    list_filter = ('status',)

# adding Booking model to admin
class BookingInline(admin.StackedInline):
    model = Booking
    can_delete = False
    verbose_name = 'Booking Details'
    verbose_name_plural = 'Booking Details'
    classes = ('collapse',)
    extra = 1
    readonly_fields = ('booking_number',)
    fields = (
        'children','number_of_children', 'number_of_adults','room_or_rooms','booking_date','check_in_date','check_out_date',
        'booking_status','payment_status','payment_method','booking_source','special_requests',
        'special_instructions','standard_rate','promotional_rate','corporate_rate','booking_number'
    )

# adding Guest model to admin
class GuestAdmin(admin.ModelAdmin):
    inlines = (
        BookingInline,
    )
    fields = ('full_name', 'gender', 'email_adress', 'phone_number', 'nin', 'address')
    list_display = ['full_name', 'phone_number', 'room_number',]
    search_fields = ['full_name',]
    def room_number(self, obj):
        # Retrieve the associated booking and then fetch the room number
        booking = obj.guest_profile  #  'guest_profile' is the OneToOneField name
        return booking.room_or_rooms.first().room_number if booking.room_or_rooms.exists() else None
    room_number.short_description = 'Room Number'





# registering models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Guest, GuestAdmin)
