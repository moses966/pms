from django.apps import AppConfig
from django.db.models.signals import pre_save


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
