from django.db import models
from management.custom_validators import validate_contact, validate_nin
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid

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
    count = models.PositiveBigIntegerField(
        help_text='number of rooms in this category.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
        max_length=3,
    )
    floor_number = models.CharField(
        null=True,
        blank=True,
        max_length=2,
        help_text='Location of the room on the building counting from the bottom level.'
    )
    description = models.TextField()
    capacity = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('out_of_service', 'Out of Service'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cleaned = models.CharField(
        max_length=15,
        default='Not yet'
    )
    # Pricing based on rate category
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

    # Discount percentage (0-100)
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
        super().save(*args, **kwargs)

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
    number_of_adults = models.PositiveIntegerField(default=1)
    room_or_rooms = models.ManyToManyField(
        Room,
        related_name='bookings',
    )
    check_in_date = models.DateTimeField(default=timezone.now)
    check_out_date = models.DateTimeField(default=timezone.now)
    booking_date = models.DateTimeField(default=timezone.now)
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    BOOKING_SOURCE = (
        ('online', 'Online'),
        ('walk_in', 'Walk-in'),
        ('phone', 'Phone Reservation'),
    )
    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='confirmed',
    )
    booking_source = models.CharField(
        null=True,
        blank=True,
        max_length=15,
        choices=BOOKING_SOURCE,
        default='walk_in',
    )
    special_requests = models.TextField(blank=True, null=True)
    special_instructions = models.TextField(
        blank=True,
        null=True,
        help_text='Special considerations or instructions to hotel staff.'
    )
    booking_number = models.CharField(max_length=4, unique=True, blank=True, null=True)
    check_in = models.BooleanField(
        default=False,
        verbose_name='Guest Has Checked In',
        help_text='Tick if guest has checked in',
    )

    def save(self, *args, **kwargs):
        if not self.booking_number:
            # Generate a unique booking number using the first 4 characters of a UUID
            self.booking_number = 'BK-' + str(uuid.uuid4())[:4]
        super().save(*args, **kwargs)
        

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
    full_name = models.CharField(
        max_length=25,
    )
    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(
        max_length=10,
        choices=GENDER,
        default='male',
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
        return self.full_name
    
# Reservation model
class Reservation(models.Model):
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField(null=True, blank=True)
    guest_contact = models.CharField(max_length=15)
    check_in_date = models.DateField()
    check_out_date = models.DateTimeField()
    room_or_rooms = models.ManyToManyField(
        Room,
        related_name='reservations',
    )
    number_of_adults = models.PositiveIntegerField(default=1)
    number_of_children = models.PositiveIntegerField(default=0)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deposit = models.BooleanField(
        default=False,
        verbose_name='Deposit Paid',
        help_text='Tick if there is any deposit payment'
    )
    deposit_amount = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ]
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default='active',
    )
    deadline = models.DateTimeField(
        help_text='Time for invalidation of reservation contract.',
        blank=True,
        null=True,
    )
    reservation_number = models.CharField(max_length=4, unique=True, blank=True, null=True)
    check_in = models.BooleanField(
        default=False,
        verbose_name='Guest Has Checked In',
        help_text='Tick if guest has checked in',
    )

    def save(self, *args, **kwargs):
        if not self.reservation_number:
            # Generate a unique reservation number using the first 4 characters of a UUID
            self.reservation_number = 'RS-' + str(uuid.uuid4())[:4]
        super().save(*args, **kwargs)

    # update reservation status if PaymentInformation Instance is saved
    def update_status_if_payment_info_exists(self):
        if self.reserve_info.exists():
            self.status = 'confirmed'
            self.save()

    def __str__(self):
        room_numbers = ", ".join(room.room_number for room in self.room_or_rooms.all())
        return f"Room: {room_numbers} - Reservation Number: {self.reservation_number}"

class PaymentInformation(models.Model):
    booking_info = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='booking_info',
        blank=True,
        null=True,
    )
    reserve_info = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='reserve_info',
        blank=True,
        null=True,
    )
    PAYMENT_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('due', 'Due'),
    )
    PAYMENT_METHOD = (
        ('cash', 'Cash'),
        ('mtn', 'Mtn MOMO'),
        ('airtel', 'Airtel Money'),
        ('bank', 'Bank transfer'),
    )
    RATE_PLAN_CHOICES = [
        ('standard', 'Standard Rate'),
        ('promotional', 'Promotional Rate'),
        ('corporate', 'Corporate Rate'),
    ]    
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='pending',
    )
    payment_method = models.CharField(
        max_length=15,
        choices=PAYMENT_METHOD,
        default='cash'
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
        if self.reserve_info:
            rooms = self.reserve_info.room_or_rooms.all()
            instance_type = "Reservation"  # Set instance_type to "Reservation"
        elif self.booking_info:
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
            elif instance_type == "Reservation":
                # Generate a receipt number using the reservation number
                self.receipt_number = self.reserve_info.reservation_number if self.reserve_info else None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt number: {self.receipt_number} - Amount Paid: {self.amount_paid}"