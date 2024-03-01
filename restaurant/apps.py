from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save


class RestaurantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant'
    verbose_name = 'Events & Occassions'

    '''def ready(self):
        from . import signals

        post_save.connect(
            signals.update_sub_total,
            sender='restaurant.FoodOrdrinks',
            dispatch_uid='update_sub_total_on_save',
        )
        post_delete.connect(
            signals.update_sub_total,
            sender='restaurant.FoodOrDrinks',
            dispatch_uid='update_sub_total_on_delete',
        )'''
