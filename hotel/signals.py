from django.dispatch import receiver
from django.utils import timezone


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

'''def mark_reservations_as_cancelled(sender, instance, **kwargs):
    if instance.pk:
        for room in instance.room_or_rooms.all():
            reservations = room.reservations.filter(status='active')
            for reservation in reservations:
                reservation.status = 'cancelled'
                reservation.save()'''
"""
def update_reservation_status(sender, instance, **kwargs):
   
    '''
    if instance.status == 'active':
        if instance.deadline and timezone.now() > instance.deadline:
            instance.status = 'cancelled'
            instance.save()'''
    '''if instance.pk:
        for room in instance.room_or_rooms.all():
            reservations = room.reservations.filter(status='active')
            for reservation in reservations:
                if timezone.now() > reservation.deadline:
                    reservation.status = 'cancelled'
                    reservation.save()'''
"""         