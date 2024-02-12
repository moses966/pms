from celery import shared_task
from django.utils import timezone
from .models import Reservation

@shared_task
def check_reservation_deadline():
    # Get all active reservations with deadlines that have passed
    expired_reservations = Reservation.objects.filter(
        status='active', deadline__lte=timezone.now()
    )

    # Update the status of each expired reservation to 'cancelled'
    for reservation in expired_reservations:
        reservation.status = 'cancelled'
        reservation.save()
