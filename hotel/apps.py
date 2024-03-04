from django.apps import AppConfig
from django.db.models.signals import  (
    post_save, post_delete, pre_save, post_migrate
)


class HotelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotel'
    verbose_name = 'Hotel Management'

    def ready(self):
        from . import signals
        from . import custom_permissions
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
        '''pre_save.connect(
            signals.update_room_status_on_booking_change,
            sender='hotel.Booking',
            dispatch_uid='update_room_status_on_booking_change',
        )
        post_save.connect(
            signals.update_room_status_on_booking_save,
            sender='hotel.Booking',
            dispatch_uid='update_room_status_on_booking_save',
        )'''
        post_migrate.connect(
            custom_permissions.create_custom_permissions,
            sender=self,
        )  
