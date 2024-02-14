from celery import shared_task
#from pytz import timezone
from django.utils import timezone as dj_timezone
from .models import Reservation, Room, Booking

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

@shared_task(name='Update_room_status')
def update_room_status():
    # Get all rooms
    rooms = Room.objects.all()

    for room in rooms:
        # Check if the room has any associated bookings or reservations
        if room.bookings.exists() or room.reservations.exists():
            # Get the check-out date and time for all associated bookings and reservations
            check_out_dates = []

            for booking in room.bookings.all():
                check_out_dates.append(booking.check_out_date)

            for reservation in room.reservations.all():
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