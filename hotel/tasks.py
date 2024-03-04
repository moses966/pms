from celery import shared_task
from django.utils import timezone
from django.db import transaction
from .models import Reservation, Room, Booking
from choices.models import RoomStatus

# this method looks for deadlines
# If caught, reservation is automatically marked 
# cancelled
'''@shared_task
def check_reservation_deadline():
    # Get all active reservations with exceeded deadlines
    reservations_to_cancel = Reservation.objects.filter(status__reservation_status='active', deadline__lt=timezone.now())

    # Cancel reservations
    for reservation in reservations_to_cancel:
        # Update status to cancelled
        cancelled_status = ReservationStatus.objects.get(reservation_status='cancelled')
        reservation.status = cancelled_status
        reservation.save()'''

# This method looks for checkout date
# If caught, room status is updated to available
#@transaction.atomic
@shared_task(name='Update Room Status on check out.')
def update_room_status():
    # Get all booking instances with booking status as "checked out" and not yet processed
    bookings_to_process = Booking.objects.filter(
        booking_status__booking_status='checked out',
        processed=False  # Filter out instances that have not been processed
    )

    # Iterate over each booking instance
    for booking in bookings_to_process:
        # Get the rooms associated with this booking
        rooms = booking.room_or_rooms.all()
        
        # Update the status of each room associated with this booking to available
        for room in rooms:
            room.status = RoomStatus.objects.get(room_status='available')
            room.save()

        # Mark the booking instance as processed
        booking.processed = True
        booking.save()

# This method implements:
# if a bboking instance is saved with booking_status=confirmed or reservation_status=confirmed,
# and, checki-in is reached or exceeded
# room status is updated to occupied else, available
@shared_task(name='Update_room_status_on_check_in')
def update_room_status_to_occupied():
    # Get all confirmed bookings with check-in date and time reached
    bookings_to_update = Booking.objects.filter(booking_status__booking_status='confirmed', check_in_date__lte=timezone.now())

    # Update room status to occupied
    for booking in bookings_to_update:
        for room in booking.room_or_rooms.all():
            occupied_status = RoomStatus.objects.get(room_status='occupied')
            room.status = occupied_status
            room.save()

    '''# Get all confirmed reservations with check-in date and time reached
    reservations_to_update = Reservation.objects.filter(status__reservation_status='confirmed', check_in_date__lte=timezone.now())

    # Update room status to occupied
    for reservation in reservations_to_update:
        for room in reservation.room_or_rooms.all():
            occupied_status = RoomStatus.objects.get(room_status='occupied')
            room.status = occupied_status
            room.save()
    return 'Check-in date detected' '''