from celery import shared_task
from django.utils import timezone
from .models import Reservation, Room, Booking
from choices.models import RoomStatus,  ReservationStatus

# this method looks for deadlines
# If caught, reservation is automatically marked 
# cancelled
@shared_task
def check_reservation_deadline():
    # Get all active reservations with exceeded deadlines
    reservations_to_cancel = Reservation.objects.filter(status__reservation_status='active', deadline__lt=timezone.now())

    # Cancel reservations
    for reservation in reservations_to_cancel:
        # Update status to cancelled
        cancelled_status = ReservationStatus.objects.get(reservation_status='cancelled')
        reservation.status = cancelled_status
        reservation.save()

# This method looks for checkout date
# If caught, room status is updated to available
@shared_task
def update_room_status():
    # Get all rooms with bookings where the checkout time is exceeded
    rooms_to_update = Room.objects.filter(bookings__check_out_date__lt=timezone.now())

    # Update room status to available
    for room in rooms_to_update:
        available_status = RoomStatus.objects.get(room_status='available')
        room.status = available_status
        room.save()

    # Get all rooms with reservations where the checkout time is exceeded
    rooms_to_update = Room.objects.filter(reservations__check_out_date__lt=timezone.now())

    # Update room status to available
    for room in rooms_to_update:
        available_status = RoomStatus.objects.get(room_status='available')
        room.status = available_status
        room.save()
    return 'Room Status Updated'
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

    # Get all confirmed reservations with check-in date and time reached
    reservations_to_update = Reservation.objects.filter(status__reservation_status='confirmed', check_in_date__lte=timezone.now())

    # Update room status to occupied
    for reservation in reservations_to_update:
        for room in reservation.room_or_rooms.all():
            occupied_status = RoomStatus.objects.get(room_status='occupied')
            room.status = occupied_status
            room.save()
    return 'Check-in date detected'