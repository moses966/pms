from django.urls import path
from .views import (
    InventoryItemListView, SupplierListView,
    TransactionDayArchiveView, InventoryItemDetailView,
    TransactionYearArchiveView, TransactionMonthArchiveView,
    TransactionDetailView,
)

urlpatterns =[
    path('items/', InventoryItemListView.as_view(), name='items'),
    path('items/item/<int:pk>/', InventoryItemDetailView.as_view(), name='item'),
    path('suppliers/', SupplierListView.as_view(), name='item_suppliers'),
    path(
        'transactions/<int:year>/<str:month>/<int:day>/',
        TransactionDayArchiveView.as_view(), name='day_transactions'
    ),
    
    path(
        "transaction-archives/<int:year>/<str:month>/",
        TransactionMonthArchiveView.as_view(),
        name="month_transaction_archives",
    ),
    path("transaction-archives/<int:year>/", TransactionYearArchiveView.as_view(), name='year_transaction_archives'),
    path(
        'transaction/<int:year>/<int:month>/<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'
    ),
]