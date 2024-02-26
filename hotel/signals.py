from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import m2m_changed
from .models import Reservation, Booking
from choices.models import ReservationStatus, RoomStatus, BookingStatus
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

# update reservation status if PaymentInformation Instance is saved
def update_reservation_status(sender, instance, **kwargs):
    if instance.reserve_info:
        instance.reserve_info.update_status_if_payment_info_exists()

# method for updating room status to confirmed
# if, reservation is confirmed and check-in date reached
def update_room_status_on_reservation(instance):
    confirmed_status = ReservationStatus.objects.get(reservation_status='confirmed')
    cancelled_status = ReservationStatus.objects.get(reservation_status='cancelled')
    occupied_status = RoomStatus.objects.get(room_status='occupied')
    available_status = RoomStatus.objects.get(room_status='available')

    # Check if check-in dates are today
    today = timezone.localdate()
    if instance.check_in_date == today and instance.status == confirmed_status:
        # Update corresponding rooms to occupied
        for room in instance.room_or_rooms.all():
            room.status = occupied_status
            room.save()

    elif instance.status == cancelled_status:
        # Update corresponding rooms to available if reservation is cancelled
        for room in instance.room_or_rooms.all():
            room.status = available_status
            room.save()

# method for updating room status to confirmed
# if, booking is confirmed and check-in date  and time reached
def update_room_status_on_booking(instance):
    confirmed_status = BookingStatus.objects.get(booking_status='confirmed')
    cancelled_status = BookingStatus.objects.get(booking_status='cancelled')
    occupied_status = RoomStatus.objects.get(room_status='occupied')
    available_status = RoomStatus.objects.get(room_status='available')

    # Check if check-in dates are today
    today = timezone.localdate()
    if (instance.check_in_date and instance.check_in_date.date() == today) and instance.booking_status == confirmed_status:
        # Update corresponding rooms to occupied
        for room in instance.room_or_rooms.all():
            room.status = occupied_status
            room.save()
    elif instance.booking_status == cancelled_status:
        # Update corresponding rooms to available if booking is cancelled
        for room in instance.room_or_rooms.all():
            room.status = available_status
            room.save()
 
def update_room_status_on_reservation_change(sender, instance, **kwargs):
    # Check if the status has changed
    if instance.pk:  # Check if the instance is already saved (i.e., has a primary key)
        old_instance = Reservation.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:
            update_room_status_on_reservation(instance)

def update_room_status_on_reservation_save(sender, instance, created, **kwargs):
    # If the instance is newly created, or the status hasn't changed,
    # proceed to update the room status
    if created or not hasattr(instance, '_changed_fields') or 'status' not in instance._changed_fields:
        update_room_status_on_reservation(instance)
    
@receiver(pre_save, sender=Booking)
def update_room_status_on_booking_change(sender, instance, **kwargs):
    # Check if the status has changed
    if instance.pk:  # Check if the instance is already saved (i.e., has a primary key)
        old_instance = Booking.objects.get(pk=instance.pk)
        if old_instance.booking_status != instance.booking_status:
            update_room_status_on_booking(instance)

@receiver(post_save, sender=Booking)
def update_room_status_on_booking_save(sender, instance, created, **kwargs):
    # If the instance is newly created, or the status hasn't changed,
    # proceed to update the room status
    if created or not hasattr(instance, '_changed_fields') or 'booking_status' not in instance._changed_fields:
        update_room_status_on_booking(instance)

@receiver(
    m2m_changed, sender=Reservation.room_or_rooms.through,
    dispatch_uid='update_payment_info_amount_paid_for_reservation',
)
def update_payment_info_amount_paid_for_reservation(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:  # Check if the M2M relationship is changed
        if instance.reserve_info.exists():  # Check if there is an associated PaymentInformation instance
            payment_info = instance.reserve_info.first()
            room_count = instance.room_or_rooms.count()
            new_amount_paid = room_count * instance.get_rate_plan()  # Recalculate amount_paid based on the rate plan
            payment_info.amount_paid = new_amount_paid
            payment_info.save()

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