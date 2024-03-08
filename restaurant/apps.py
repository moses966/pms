from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save


class RestaurantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant'
    verbose_name = 'Events & Occassions'
