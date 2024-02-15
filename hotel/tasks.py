from celery import shared_task
from django.utils import timezone as dj_timezone
from .models import Reservation, Room, Booking

# this method looks for deadlines
# If caught, reservation is automatically marked 
# cancelled
@shared_task
def check_reservation_deadline():
    # Get all active reservations with deadlines that have passed
    expired_reservations = Reservation.objects.filter(
        status='active', deadline__lte=dj_timezone.now()
    )

    # Update the status of each expired reservation to 'cancelled'
    for reservation in expired_reservations:
        reservation.status = 'cancelled'
        reservation.save()

# This method looks for checkout date
# If caught, room status is updated to available
@shared_task(name='Update_room_status')
def update_room_status():
    # Get all rooms
    rooms = Room.objects.all()

    for room in rooms:
        # Check if the room has any associated bookings or reservations
        if room.bookings.filter(booking_status__in=['confirmed']).exists() or \
                room.reservations.filter(status='confirmed').exists():
            check_out_dates = []
            
            # Filter bookings with status not cancelled
            bookings = room.bookings.exclude(booking_status='cancelled')
            for booking in bookings:
                check_out_dates.append(booking.check_out_date)

            # Filter reservations with status confirmed
            reservations = room.reservations.filter(status='confirmed')
            for reservation in reservations:
                check_out_dates.append(reservation.check_out_date)

            # Check if the current date and time exceed any of the check-out dates and times
            current_datetime = dj_timezone.now()

            for check_out_date in check_out_dates:
                if current_datetime >= check_out_date:
                    # Update room status to available
                    room.status = 'available'
                    room.save()
                    break  # No need to continue checking if one check-out date is exceeded

    return 'Room statuses updated'

# This method implements:
# if a bboking instance is saved with booking_status=confirmed, 
# room status is updated to occupied else, available
@shared_task(name='Update_room_status_with_confirmation')
def update_room_statuses():
    # Get all rooms
    rooms = Room.objects.all()

    for room in rooms:
        # Check if the room has any associated bookings with status 'confirmed'
        if room.bookings.filter(booking_status='confirmed').exists():
            # Update room status to 'occupied'
            room.status = 'occupied'
            room.save()
        else:
            # Update room status to 'available'
            room.status = 'available'
            room.save()

    return 'Confirmed Room statuses updated'