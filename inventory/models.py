from django.db import models
from django.utils import timezone

class Supplier(models.Model):
    name = models.CharField(max_length=60)
    contact_person = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.name} - {self.location}"

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity_on_hand = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Total number of this Item Received.',
        default=0,
    )
    units = models.CharField(max_length=10, blank=True, null=True, help_text="E.g Kgs, meters, pieces")
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Number of Items already found in the store.'
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    total_in_store = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateField(default=timezone.now)
    delivery_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Purchase Order #{self.pk} - {self.supplier.name}"

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    def save(self, *args, **kwargs):
        # Calculate sub total quantity
        self.sub_total = self.unit_price * self.quantity_ordered
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory_item.name} - Qty: {self.quantity_ordered}"

class InventoryTransaction(models.Model):
    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    TRANSACTION_TYPE = [
        ('consumption', 'Consumption'),
        ('transfer', 'Transfer'),
    ]
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(
        max_length=15,
        choices=TRANSACTION_TYPE,
    )
    quantity = models.DecimalField(
        max_digits=10,
        default=0,
        decimal_places=2
    )
    remarks = models.TextField(
        blank=True,
        null=True
    )
    available_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    

    def __str__(self):
        return f"{self.transaction_type} - {self.inventory_item.name}"

    class Meta:
        verbose_name = "Inventory Transaction"
        verbose_name_plural = "Inventory Transactions"
