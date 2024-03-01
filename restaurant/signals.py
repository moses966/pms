from django.db import models
from django.db.models.signals import post_delete
from .models import FoodOrDrinks
from django.dispatch import receiver

'''def update_sub_total(sender, instance, **kwargs):
    booking_or_reservation = None
    if instance.booking_guest:
        booking_or_reservation = instance.booking_guest
    elif instance.reserving_guest:
        booking_or_reservation = instance.reserving_guest

    if booking_or_reservation:
        # Aggregate the subtotal of all FoodOrDrinks instances associated with the booking or reservation
        sub_total = booking_or_reservation.booking_food.aggregate(total=models.Sum(models.F('quantity') * models.F('food_or_drink__unit_price')))['total'] or 0
        booking_or_reservation.sub_total_amount = sub_total
        booking_or_reservation.save()'''
'''@receiver(post_delete, sender=FoodOrDrinks)
def update_cumulative_amount_on_delete(sender, instance, **kwargs):
    """
    Signal handler to update the cumulative amount when a FoodOrDrinks instance is deleted.
    """
    instance.update_cumulative_amount()'''