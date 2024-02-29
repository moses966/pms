from django.db import models
from choices.models import MenuAndDrinksChoice, ServiceChoices
from hotel.models import Room, Guest, Booking, Reservation

class FoodOrDrinks(models.Model):
    booking_guest = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='booking_food',
        blank=True,
        null=True,
    )
    reserving_guest = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='reserving_food',
        blank=True,
        null=True,
    )
    food_or_drink = models.ForeignKey(
        MenuAndDrinksChoice,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField()
    sub_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Events(models.Model):
    customer_name = models.CharField(max_length=25)
    mobile_contact = models.CharField(max_length=25)
    service = models.ForeignKey(
        ServiceChoices,
        on_delete=models.CASCADE,
    )
    reservation_date = models.DateTimeField(auto_now_add=True)
    number_of_days = models.IntegerField()
    number_of_guests = models.IntegerField()
    sub_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class Meta:
        verbose_name = 'Event or Occassion'
        verbose_name_plural = 'Event or Occassion'