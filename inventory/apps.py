from django.apps import AppConfig
from django.db.models.signals import post_save, pre_delete, pre_save


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    def ready(self):
        from . import signals
        '''
          Connect signal handlers to the appropriate signals
        '''
        # update purchase order total cost after saving instance
        post_save.connect(
            signals.update_purchase_order_total_cost,
            sender='inventory.PurchaseOrderItem',
            dispatch_uid='update_purchase_order_total_cost',
        )
        # update total_cost after deleting purchase order item
        pre_delete.connect(
            signals.delete_purchase_order_item,
            sender='inventory.PurchaseOrderItem',
            dispatch_uid='delete_purchase_order_item',
        )
        
