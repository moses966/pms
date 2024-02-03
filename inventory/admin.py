from django.contrib import admin
from .models import (
    Supplier, InventoryItem,
    PurchaseOrder, PurchaseOrderItem,
    InventoryTransaction,
)

class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    readonly_fields = ('sub_total',)
    can_delete = False
    extra = 1

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'supplier', 'order_date', 'delivery_date', 'total_cost',)
    search_fields = ['delivery_date',]
    readonly_fields = ('total_cost',)
    list_filter = ['supplier']
    inlines = [PurchaseOrderItemInline]

class InventoryTransactionInline(admin.StackedInline):
    model = InventoryTransaction
    can_delete = False
    extra = 1

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'quantity_on_hand', 'units', 'supplier', 'total_in_store')
    search_fields = ['name']
    list_filter = ['name']
    readonly_fields = ('total_in_store',)
    inlines = [InventoryTransactionInline]

class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'transaction_type', 'quantity', 'transaction_date', 'available_quantity',)
    list_filter = ('inventory_item',)
    readonly_fields = ('available_quantity',)
    search_fields = ['transaction_date', 'transaction_type']

class supplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone_number',)
    list_filter = ('name', 'location',)
    search_fields = ['name']

admin.site.register(Supplier, supplierAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(InventoryTransaction, InventoryTransactionAdmin)

