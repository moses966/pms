from django.db import models
from management.custom_validators import validate_contact, validate_nin
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid
from choices.models import (
    RoomStatus,
    BookingSource, BookingStatus, GenderChoices,
    PaymentStatus, PaymentMethod,
)

# Room category class
class Category(models.Model):
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    capacity = models.PositiveIntegerField()
    room_count = models.PositiveIntegerField(
        help_text='number of rooms in this category.',
        default=0,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_room_count(self):
        self.room_count = self.room_set.count()
        self.save()
    class Meta:
        verbose_name = "Room Category"
        verbose_name_plural = "Room Categories"
    
    def __str__(self):
        return self.name
# Rooms model
class Room(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=30,
    )
    room_number = models.CharField(
        null=True,
        blank=True,
        max_length=20,
    )
    floor_number = models.CharField(
        null=True,
        blank=True,
        max_length=2,
        help_text='Location of the room on the building counting from the bottom level.'
    )
    description = models.TextField()
    capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    status = models.ForeignKey(
        RoomStatus,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cleaned = models.CharField(
        max_length=15,
        default='Not yet'
    )
    standard_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    promotional_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    corporate_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='Discount percentage (0-100)',
    )
    def save(self, *args, **kwargs):
        # Automatically calculate promotional price based on standard price and discount
        if self.standard_price is not None and self.discount is not None:
            self.promotional_price = self.standard_price - (self.discount / 100 * self.standard_price)
        # Check if the room is being saved for the first time (creating a new room)
        is_new_room = not self.pk
        super().save(*args, **kwargs)
        # If the room is new, increment the room count for the category
        if is_new_room:
            self.category.update_room_count()
        
    def delete(self, *args, **kwargs):
        # Store the category before deleting the room
        category = self.category
        super().delete(*args, **kwargs)
        # Decrement the room count for the category after deleting the room
        category.update_room_count()

    def __str__(self):
        return f"{self.name} - Room No. {self.room_number}"

# Booking model
class Booking(models.Model):
    children = models.BooleanField(
        default=False,
        verbose_name='Children.',
        help_text='Tick if there are children among guests.'
    )
    number_of_children = models.PositiveIntegerField(default=0)
    number_of_adults = models.PositiveIntegerField(default=2)
    room_or_rooms = models.ManyToManyField(
        Room,
        related_name='bookings',
    )
    check_in_date = models.DateTimeField(default=timezone.now)
    check_out_date = models.DateTimeField()
    booking_date = models.DateField(default=timezone.now, blank=False, null=False)
    booking_time = models.TimeField(auto_now_add=True)
    booking_status = models.ForeignKey(
        BookingStatus,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    booking_source = models.ForeignKey(
        BookingSource,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    special_requests = models.TextField(blank=True, null=True)
    special_instructions = models.TextField(
        blank=True,
        null=True,
        help_text='Special considerations or instructions to hotel staff.'
    )
    booking_number = models.CharField(max_length=4, unique=True, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    processed = models.BooleanField(default=False)
    def get_rate_plans(self):
        if self.booking_info.exists():
            payment_info = self.booking_info.first()  # Get the first PaymentInformation instance
            room_count = self.room_or_rooms.count()
            if room_count > 0:
                return payment_info.amount_paid / room_count
        return 0
    
    @property
    def total_bill(self):
        food_or_drinks_cumulative = self.booking_food.last().cumulative_amount if self.booking_food.exists() else 0
        other_services_cumulative = self.booking_service.last().cumulative_amount if self.booking_service.exists() else 0
        total_amount_paid = self.booking_info.amount_paid if self.booking_info else 0
        return food_or_drinks_cumulative + other_services_cumulative + total_amount_paid

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def save(self, *args, **kwargs):
        if not self.booking_number:
            # Generate a unique booking number using the first 4 characters of a UUID
            self.booking_number = 'BK-' + str(uuid.uuid4())[:4]
        super().save(*args, **kwargs)
        self.update_total_bill()
        

    def __str__(self):
        room_numbers = ", ".join(room.room_number for room in self.room_or_rooms.all())
        return f"Room: {room_numbers}  - {self.booking_date}"
    
# Guest model
class Guest(models.Model):
    guest_profile = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='guest_profile',
    )
    first_name = models.CharField(
        max_length=17,
    )
    given_name = models.CharField(max_length=17)
    gender = models.ForeignKey(
        GenderChoices,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    email_adress = models.EmailField(
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        max_length = 10,
        validators=[validate_contact],
    )
    nin = models.CharField(
        max_length=14,
        validators=[validate_nin],
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=60,
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.first_name} {self.given_name}"

class PaymentInformation(models.Model):
    booking_info = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='booking_info',
        blank=True,
        null=True,
    )
    payment_status = models.ForeignKey(
        PaymentStatus,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Currency: Ugx'
    )
    #reciept_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    standard_rate = models.BooleanField('Standard Rate', default=False)
    promotional_rate = models.BooleanField('Promotional Rate', default=False)
    corporate_rate = models.BooleanField('Corporate Rate', default=False)
    receipt_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    def clean(self):
        # Ensure only one rate plan is selected
        rate_plan_count = sum([self.standard_rate, self.promotional_rate, self.corporate_rate])
        if rate_plan_count != 1:
            raise ValidationError("Select exactly one rate plan.")
    def save(self, *args, **kwargs):
        instance_type = None  # Default to None
        if self.booking_info:
            rooms = self.booking_info.room_or_rooms.all()
            instance_type = "Booking"  # Set instance_type to "Booking"
        else:
            rooms = None

        if rooms:
            room_prices = []
            for room in rooms:
                if self.standard_rate:
                    room_prices.append(room.standard_price)
                elif self.promotional_rate:
                    room_prices.append(room.promotional_price)
                elif self.corporate_rate:
                    room_prices.append(room.corporate_price)
                else:
                    room_prices.append(0)  # Default to 0 if no rate plan selected
            self.amount_paid = sum(room_prices)
        else:
           self.amount_paid = 0  # Handle case when no room is associated

        # assigning a receipt number
        if not self.receipt_number:
            if instance_type == "Booking":
                # Generate a receipt number using the booking number
                self.receipt_number = self.booking_info.booking_number if self.booking_info else None
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Receipt number: {self.receipt_number} - Amount Paid: {self.amount_paid}"