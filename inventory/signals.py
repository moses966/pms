from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Sum

from .models import PurchaseOrderItem

@receiver(post_save, sender=PurchaseOrderItem)
def update_purchase_order_total_cost(sender, instance, created, **kwargs):
    if created:  # Only update total cost if a new PurchaseOrderItem was created
        purchase_order = instance.purchase_order
        # Recalculate total cost by summing up all subtotals of related PurchaseOrderItems
        total_cost = purchase_order.purchaseorderitem_set.aggregate(total_cost=Sum('sub_total'))['total_cost'] or 0
        purchase_order.total_cost = total_cost
        purchase_order.save()

@receiver(pre_delete, sender=PurchaseOrderItem)
def delete_purchase_order_item(sender, instance, **kwargs):
    purchase_order = instance.purchase_order
    # Recalculate total cost by excluding the sub_total of the item being deleted
    total_cost = purchase_order.total_cost - instance.sub_total
    purchase_order.total_cost = total_cost if total_cost >= 0 else 0
    purchase_order.save()
