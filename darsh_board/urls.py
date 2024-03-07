from django.urls import path
from .views import (
    HomePageView, InvoiceDetailView, 
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('invoice/<int:pk>/<str:booking_number>/', InvoiceDetailView.as_view(), name='invoice'),
]
