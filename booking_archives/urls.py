from django.urls import path
from .views import (
    BookingDetailView,
    BookingMonthArchiveView,
    BookingYearArchiveView,
    CustomTodayArchiveView,
    BookingWeekArchiveView,
)

urlpatterns = [
    path('bookings/today/', CustomTodayArchiveView.as_view(), name='booking_today_archive'),
    path('bookings/yearly/', BookingYearArchiveView.as_view(), name='yearly_archives'),
    path('bookings/<int:year>/', BookingMonthArchiveView.as_view(), name='monthly_archives'),
    path('booking/<int:year>/<int:month>/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path(
        "<int:year>/week/<int:week>/",
        BookingWeekArchiveView.as_view(),
        name="archive_week",
    ),
]
