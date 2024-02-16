from django.contrib import admin
from .models import (
    Supplier, InventoryItem,
    PurchaseOrder, PurchaseOrderItem,
    InventoryTransaction,
)

class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    readonly_fields = ('sub_total',)
    can_delete = True
    extra = 1

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'supplier', 'order_date', 'delivery_date', 'total_cost',)
    search_fields = ['delivery_date',]
    readonly_fields = ('total_cost',)
    list_filter = ['supplier']
    inlines = [PurchaseOrderItemInline]

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'quantity_on_hand', 'units',
            'initial_total_in_store', 'current_total_in_store', 'date',
    )
    search_fields = ['name']
    list_filter = ['name']
    fields = [
        'name', 'description', 'quantity_on_hand', 'units', 'balance', 'supplier'
    ]
    readonly_fields = ('current_total_in_store', 'initial_total_in_store',)
    def current_total_in_store(self, obj):
        return obj.total_in_store

class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'transaction_type', 'quantity', 'transaction_date',)
    list_filter = ('inventory_item',)
    search_fields = ['transaction_date', 'transaction_type']

class supplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone_number',)
    list_filter = ('name', 'location',)
    search_fields = ['name']

admin.site.register(Supplier, supplierAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(InventoryTransaction, InventoryTransactionAdmin)


