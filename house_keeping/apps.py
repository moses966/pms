from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save, pre_delete


class HouseKeepingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'house_keeping'
    verbose_name = 'House keeping'

    def ready(self):
        from . import signals
        '''
          Connect signal handlers to the appropriate signals
        '''
        pre_save.connect(
            signals.delete_previous_task,
            sender='house_keeping.HouseKeepingTask',
            dispatch_uid='delete_previous_task',
        )
        post_save.connect(
            signals.add_room_to_clean_rooms,
            sender='house_keeping.MaintenanceRequest',
            dispatch_uid='add_room_to_clean_rooms',
        )
        post_save.connect(
            signals.remove_room_from_clean_rooms,
            sender='house_keeping.HouseKeepingTask',
            dispatch_uid='remove_room_from_clean_rooms',
        )
        post_save.connect(
            signals.restore_room_to_clean_rooms,
            sender='house_keeping.HouseKeepingTask',
            dispatch_uid='restore_room_to_clean_rooms',
        )
