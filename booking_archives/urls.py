from django.urls import path
from .views import (
    BookingDetailView,
    BookingMonthArchiveView,
    BookingYearArchiveView,
    CustomTodayArchiveView,
    BookingWeekArchiveView,
    BookingDayArchiveView,
)

urlpatterns = [
    path('latest/', CustomTodayArchiveView.as_view(), name='booking_latest_archive'),
    path('yearly/', BookingYearArchiveView.as_view(), name='yearly_archives'),
    path('<int:year>/', BookingMonthArchiveView.as_view(), name='monthly_archives'),
    path('booking/<int:year>/<int:month>/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path(
        "<int:year>/week/<int:week>/",
        BookingWeekArchiveView.as_view(),
        name="archive_week",
    ),
    path(
        "<int:year>/<str:month>/<int:day>/",
        BookingDayArchiveView.as_view(),
        name="archive_day",
    ),
]
