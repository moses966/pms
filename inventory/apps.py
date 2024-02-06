from django.apps import AppConfig
from django.db.models.signals import post_save, pre_delete


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    def ready(self):
        from . import signals
        # Connect signal handlers to the appropriate signals
        post_save.connect(
            signals.update_purchase_order_total_cost,
            sender='inventory.PurchaseOrderItem',
            dispatch_uid='update_purchase_order_total_cost',
        )
        pre_delete.connect(
            signals.delete_purchase_order_item,
            sender='inventory.PurchaseOrderItem',
            dispatch_uid='delete_purchase_order_item',
        )
