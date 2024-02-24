from django.views.generic import ListView, DetailView
from django.views.generic.dates import DayArchiveView, MonthArchiveView, YearArchiveView
from django.urls import reverse_lazy, reverse
from .models import Supplier, InventoryItem, PurchaseOrder, PurchaseOrderItem, InventoryTransaction

class SupplierListView(ListView):
    model = Supplier
    template_name = 'supplier_list.html'
    context_object_name = 'suppliers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class InventoryItemListView(ListView):
    model = InventoryItem
    template_name = 'inventoryitem_list.html'
    context_object_name = 'inventory_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class InventoryItemDetailView(DetailView):
    model = InventoryItem
    template_name = 'inventory/inventoryitem_details.html'
    context_object_name = 'inventory_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context
    
class TransactionDayArchiveView(DayArchiveView):
    model = InventoryTransaction
    queryset = InventoryTransaction.objects.all()
    date_field = "creation_date"
    template_name = 'inventory/daily_transactions.html'
    allow_empty = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context
    
class TransactionYearArchiveView(YearArchiveView):
    model = InventoryTransaction
    queryset = InventoryTransaction.objects.all()
    date_field = "creation_date"
    template_name = 'inventory/inventorytransaction_archive_year.html'
    make_object_list = True
    allow_empty = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class TransactionMonthArchiveView(MonthArchiveView):
    model = InventoryTransaction
    queryset = InventoryTransaction.objects.all()
    date_field = "creation_date"
    template_name = 'inventory/monthly_transactions.html'
    allow_empty = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class TransactionDetailView(DetailView):
    model = InventoryTransaction
    template_name = 'inventory/transaction_details.html'
    context_object_name = 'transaction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['home_url'] = reverse('home')
        return context