from django.contrib import admin
from django.utils import timezone
from django.contrib.auth import get_permission_codename
from .models import Room, Category, Guest, Booking, PaymentInformation
from house_keeping.models import CleanRoom
from restaurant.models import FoodOrDrinks, OtherService
from django.db import models

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
         'standard_price', 'corporate_price', 'status', 'get_last_cleaned']
    search_fields = ['name', 'capacity', 'status']
    list_filter = ('status', 'floor_number',)
    readonly_fields = ('promotional_price',)

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
    max_num = 1
    readonly_fields = ('amount_paid',)
    fields = (
        'payment_status','payment_method', 'standard_rate','promotional_rate',
        'corporate_rate', 'amount_paid',
    )

# adding FoodOrDrinks to admin
class FoodOrDrinksInline(admin.TabularInline):
    model = FoodOrDrinks
    fields = ('food_or_drink', 'quantity', 'sub_total_amount', 'cumulative_amount',)
    can_delete = False
    verbose_name = 'Food And Drinks'
    verbose_name_plural = 'Food and Drinks'
    classes = ('collapse',)
    extra = 0
    readonly_fields = ('sub_total_amount', 'cumulative_amount',)

# adding Additional services to admin
class OtherServiceInline(admin.TabularInline):
    model = OtherService
    fields = ('service', 'number_of_users', 'number_of_times', 'sub_total_amount', 'cumulative_amount')
    can_delete = False
    verbose_name = 'Additional Service'
    verbose_name_plural = 'Additional Services'
    classes = ('collapse',)
    extra = 0
    readonly_fields = ('sub_total_amount', 'cumulative_amount',)

class GuestInline(admin.StackedInline):
    model = Guest
    classes = ('collapse',)
    can_delete = False
    extra = 1
    fields = ('first_name', 'given_name', 'gender', 'email_adress', 'phone_number', 'nin', 'address')

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.has_perm('hotel.view_sensitive_fields'):
            fields = [field for field in fields if field != 'full_name']
        return fields

# adding Booking model to admin
class BookingAdmin(admin.ModelAdmin):
    verbose_name = 'Booking Details'
    verbose_name_plural = 'Booking Details'
    readonly_fields = ('booking_number',)
    search_fields = ('booking_date', 'booking_number',)
    fields = (
        'children','number_of_children', 'number_of_adults','room_or_rooms', 'number_of_days','booking_date','check_in_date','check_out_date',
        'booking_status', 'booking_source','special_requests',
        'special_instructions','booking_number',
    )
    inlines = (
        GuestInline,
        PaymentInformationInline,
        FoodOrDrinksInline,
        OtherServiceInline,
    )
    list_filter = [
        'room_or_rooms', 'booking_status',
    ]
    # Define list display with desired fields
    list_display = ('get_guest_full_name', 'get_guest_phone_number',
        'get_room_number', 'number_of_days', 'booking_number', 'booking_status', 'get_amount_paid',
    )
    def get_readonly_fields(self, request, obj=None):
        # List of fields that should be read-only
        readonly_fields = ['booking_number']
        # Check if the current user has the required permission
        if request.user.has_perm('hotel.delete_booking'):
            # User has permission to delete, so no fields need to be read-only
            pass
        else:
            # User doesn't have permission to delete, make all fields read-only
            readonly_fields = [
                'children','number_of_children', 'number_of_adults','room_or_rooms','booking_date','check_in_date','check_out_date',
                'booking_status', 'check_in', 'booking_source','special_requests',
                'special_instructions','booking_number',
            ]
        return readonly_fields
    # Define a method named get_form which takes the parameters:
    # self: The instance of the class.
    # request: The HTTP request object containing metadata about the request.
    # obj: The object being edited on the admin page, if any.
    # **kwargs: Any additional keyword arguments passed to the method.
    def get_form(self, request, obj=None, **kwargs):
        # Call the get_form method of the superclass (the parent class of BookingAdmin),
        # passing the request, obj, and any additional keyword arguments.
        form = super().get_form(request, obj, **kwargs)
        # Set the 'request' attribute of the form to the request object.
        form.request = request
        # Return the modified form.
        return form
    def get_queryset(self, request):
        # Store the request object as an attribute of the admin instance
        self.request = request
        return super().get_queryset(request)

    def get_guest_full_name(self, obj):
        """
        Retrieves the full name of the guest associated with the given object.
        Args:
            obj: The object (typically a Booking) for which to retrieve the guest full name.
        Returns:
            str: The full name of the guest if the current user has delete permission for the model,
            otherwise returns 'Open'.
        """
        # Check if the admin instance has access to the request object
        user = self.request.user if hasattr(self, 'request') else None
        # Check if the user has delete permission for the model
        if user and user.has_perm(self.model._meta.app_label + '.' + get_permission_codename('delete', self.model._meta)):
            # Return the full name of the guest if available, otherwise None
            return f"{obj.guest_profile.first_name} {obj.guest_profile.given_name}" if obj.guest_profile else None
        else:
            return 'Open'
        

    def get_guest_phone_number(self, obj):
        user = self.request.user if hasattr(self, 'request') else None
        if user and user.has_perm(self.model._meta.app_label + '.' + get_permission_codename('delete', self.model._meta)):
            return obj.guest_profile.phone_number if obj.guest_profile else None
        else:
            return '********'
    def get_room_number(self, obj):
        room_numbers = ", ".join(room.room_number for room in obj.room_or_rooms.all())
        return room_numbers if room_numbers else None
    
    def get_amount_paid(self, obj):
        user = self.request.user if hasattr(self, 'request') else None
        if user and user.has_perm(self.model._meta.app_label + '.' + get_permission_codename('delete', self.model._meta)):
            payment_info = obj.booking_info.first()  # Get the first PaymentInformation instance associated with the booking
            return payment_info.amount_paid if payment_info else None
        else:
            return '******'

    # Customize column headers if needed
    get_guest_full_name.short_description = 'Guest Full Name'
    get_guest_phone_number.short_description = 'Guest Phone Number'
    get_room_number.short_description = 'Room Number'
    get_amount_paid.short_description = 'Room(s) Amount Paid'

# registering models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)