from django.dispatch import receiver
from django.utils import timezone
import datetime
from django.db.models.signals import m2m_changed
from .models import Booking
from choices.models import RoomStatus, BookingStatus
from django.db.models.signals import  post_save, post_delete, pre_save


def update_room_cleaned(sender, instance, **kwargs):
    # Update the corresponding Room instance's cleaned field to 'Yes'
    instance.room.cleaned = 'Yes'
    instance.room.save()

def update_room_cleaned_on_delete(sender, instance, **kwargs):
    # Check if the corresponding Room instance exists
    if instance.room:
        # Update the cleaned field to 'Not yet' upon deletion of the CleanRoom instance
        instance.room.cleaned = 'Not yet'
        instance.room.save()
@receiver(
    m2m_changed, sender=Booking.room_or_rooms.through,
    dispatch_uid='update_payment_info_amount_paid_for_booking',
)
def update_payment_info_amount_paid_for_booking(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:  # Check if the M2M relationship is changed
        if instance.booking_info.exists():  # Check if there is an associated PaymentInformation instance
            payment_info = instance.booking_info.first()
            room_count = instance.room_or_rooms.count()
            new_amount_paid = room_count * instance.get_rate_plans()  # Recalculate amount_paid based on the rate plan
            payment_info.amount_paid = new_amount_paid
            payment_info.save()