from django.apps import AppConfig
from django.db.models.signals import  post_save, post_delete


class HotelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotel'
    verbose_name = 'Hotel Management'

    def ready(self):
        from . import signals
        '''
          Connect signal handlers to the appropriate signals
        '''
        post_save.connect(
            signals.update_room_cleaned,
            sender='house_keeping.CleanRoom',
            dispatch_uid='update_room_cleaned',
        )
        post_delete.connect(
            signals.update_room_cleaned_on_delete,
            sender='house_keeping.CleanRoom',
            dispatch_uid='update_room_cleaned_on_delete',
        )
        '''
        post_save.connect(
            signals.mark_reservations_as_cancelled,
            sender='hotel.Booking',
            dispatch_uid='mark_reservations_as_cancelled',
        )
        post_save.connect(
            signals.update_reservation_status,
            sender='hotel.Reservation',
            dispatch_uid='update_reservation_status',
        )'''
