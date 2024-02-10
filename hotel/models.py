from django.db import models
from management.custom_validators import validate_contact, validate_nin
from django.utils import timezone
from django.core.exceptions import ValidationError


# Guest model
class Guest(models.Model):
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
    price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2,
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

    def __str__(self):
        return f"{self.name} - Room No. {self.room_number}"

# Booking model
class Booking(models.Model):
    guest_profile = models.OneToOneField(
        Guest,
        on_delete=models.CASCADE,
        related_name='guest_profile',
    )
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
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
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
    BOOKING_SOURCE = (
        ('online', 'Online'),
        ('walk_in', 'Walk-in'),
        ('phone', 'Phone Reservation'),
    )
    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )
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
    RATE_PLAN_CHOICES = [
        ('standard', 'Standard Rate'),
        ('promotional', 'Promotional Rate'),
        ('corporate', 'Corporate Rate'),
    ]
    standard_rate = models.BooleanField('Standard Rate', default=False)
    promotional_rate = models.BooleanField('Promotional Rate', default=False)
    corporate_rate = models.BooleanField('Corporate Rate', default=False)

    def clean(self):
        # Ensure only one rate plan is selected
        rate_plan_count = sum([self.standard_rate, self.promotional_rate, self.corporate_rate])
        if rate_plan_count != 1:
            raise ValidationError("Select exactly one rate plan.")
    
    booking_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate booking number based on guest's primary key and current timestamp
            guest_pk = self.guest_profile.pk
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.booking_number = f'BK-{guest_pk}-{timestamp}'
        super().save(*args, **kwargs)


    def __str__(self):
        room_numbers = ", ".join(room.room_number for room in self.room_or_rooms.all())
        return f"Room: {room_numbers} - {self.guest_profile} - {self.booking_date}"
    
# Reservation model
class Reservation(models.Model):
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField(null=True, blank=True)
    guest_contact = models.CharField(max_length=15)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
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
    deposit_amount = models.FloatField(default=0)
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

    def __str__(self):
        return f"Reservation for {self.guest_name} - Room: {self.room_or_rooms}"