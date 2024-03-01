from django.db import models
from choices.models import MenuAndDrinksChoice, ServiceChoices
from hotel.models import Room, Guest, Booking, Reservation
from django.db.models import Sum

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
    cumulative_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.sub_total_amount = self.food_or_drink.unit_price * self.quantity

        if self.booking_guest:
            self.cumulative_amount = (self.booking_guest.booking_food.aggregate(total=models.Sum('sub_total_amount'))['total'] or 0) + self.sub_total_amount
        elif self.reserving_guest:
            self.cumulative_amount = (self.reserving_guest.reserving_food.aggregate(total=models.Sum('sub_total_amount'))['total'] or 0) + self.sub_total_amount

        super(FoodOrDrinks, self).save(*args, **kwargs)
class Events(models.Model):
    customer_name = models.CharField(max_length=25)
    mobile_contact = models.CharField(max_length=25)
    service = models.ForeignKey(
        ServiceChoices,
        on_delete=models.CASCADE,
    )
    reservation_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()
    number_of_days = models.IntegerField()
    number_of_guests = models.IntegerField()
    sub_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class Meta:
        verbose_name = 'Event or Occassion'
        verbose_name_plural = 'Event or Occassion'