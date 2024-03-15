from django.views.generic import ListView, DetailView
from django.views.generic.dates import DayArchiveView, MonthArchiveView, YearArchiveView
from django.urls import reverse_lazy, reverse
from .models import Supplier, InventoryItem, InventoryTransaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
class SupplierListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Supplier
    template_name = 'supplier_list.html'
    context_object_name = 'suppliers'
    permission_required = 'inventory.view_supplier'

    def handle_no_permission(self):
        return render(self.request, 'errors/403.html', status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class InventoryItemListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'inventoryitem_list.html'
    context_object_name = 'inventory_items'
    permission_required = 'inventory.view_inventoryitem'

    def handle_no_permission(self):
        return render(self.request, 'errors/403.html', status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class InventoryItemDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = InventoryItem
    template_name = 'inventory/inventoryitem_details.html'
    context_object_name = 'inventory_item'
    permission_required = 'inventory.view_inventoryitem'

    def handle_no_permission(self):
        return render(self.request, 'errors/403.html', status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context
    
class TransactionDayArchiveView(LoginRequiredMixin, PermissionRequiredMixin, DayArchiveView):
    model = InventoryTransaction
    queryset = InventoryTransaction.objects.all()
    date_field = "creation_date"
    template_name = 'inventory/daily_transactions.html'
    allow_empty = True
    allow_future = True
    permission_required = 'inventory.view_inventorytransaction'

    def handle_no_permission(self):
        return render(self.request, 'errors/403.html', status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context
    
class TransactionYearArchiveView(LoginRequiredMixin, PermissionRequiredMixin, YearArchiveView):
    model = InventoryTransaction
    queryset = InventoryTransaction.objects.all()
    date_field = "creation_date"
    template_name = 'inventory/inventorytransaction_archive_year.html'
    make_object_list = True
    allow_empty = True
    allow_future = True
    permission_required = 'inventory.view_inventorytransaction'

    def handle_no_permission(self):
        return render(self.request, 'errors/403.html', status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class TransactionMonthArchiveView(LoginRequiredMixin, PermissionRequiredMixin, MonthArchiveView):
    model = InventoryTransaction
    queryset = InventoryTransaction.objects.all()
    date_field = "creation_date"
    template_name = 'inventory/monthly_transactions.html'
    allow_empty = True
    allow_future = True
    permission_required = 'inventory.view_inventorytransaction'

    def handle_no_permission(self):
        return render(self.request, 'errors/403.html', status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class TransactionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = InventoryTransaction
    template_name = 'inventory/transaction_details.html'
    context_object_name = 'transaction'
    permission_required = 'inventory.view_inventorytransaction'

    def handle_no_permission(self):
        return render(self.request, 'errors/403.html', status=403)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['home_url'] = reverse('home')
        return context