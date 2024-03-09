from celery import shared_task
import datetime
from django.db import transaction
from .models import Room, Booking
from choices.models import RoomStatus


# This method looks for checkout date
# If caught, room status is updated to available
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

@shared_task(name='Update room on check in')
def update_room_statuse():
    current_date_time = datetime.date.today()

    # Get bookings with active status and check-in date as current date
    active_bookings = Booking.objects.filter(
        booking_status__booking_status='active',
        check_in_date__date=current_date_time
    )

    # Update associated room status to reserved
    for booking in active_bookings:
        for room in booking.room_or_rooms.all():
            room.status = RoomStatus.objects.get(room_status='reserved')
            room.save()

    # Get bookings with checked in status
    checked_in_bookings = Booking.objects.filter(
        booking_status__booking_status='checked in'
    )
    # Update associated room status to occupied
    for booking in checked_in_bookings:
        for room in booking.room_or_rooms.all():
            room.status = RoomStatus.objects.get(room_status='occupied')
            room.save()

    # Get bookings with cancelled status
    cancelled_bookings = Booking.objects.filter(
        booking_status__booking_status='cancelled'
    )
    # Update room status to available if associated booking status is cancelled and room status is reserved
    for booking in cancelled_bookings:
        for room in booking.room_or_rooms.all():
            if room.status.room_status == 'reserved':
                room.status = RoomStatus.objects.get(room_status='available')
                room.save()
