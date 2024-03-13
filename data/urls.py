from django.urls import path
from .views import (
    MonthlyBookingStatisticsList,
)
urlpatterns = [
    path('monthly-total/', MonthlyBookingStatisticsList.as_view(), name='monthly_booking_statistics_list'),
]