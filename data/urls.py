from django.urls import path
from .views import (
    MonthlyBookingStatisticsList, GenderStatisticsAPIView,
)
urlpatterns = [
    path('monthly-total/', MonthlyBookingStatisticsList.as_view(), name='monthly_booking_statistics_list'),
    path('guests/gender/', GenderStatisticsAPIView.as_view(), name='gender_statistics_api'),
]