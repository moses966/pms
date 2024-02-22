from django.urls import path
from .views import (
    BookingDetailView, BookingYearArchiveView,
    BookingMonthArchiveView,
    BookingYearArchiveView,
    BookingWeekArchiveView,
    BookingDayArchiveView,
)

urlpatterns = [
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
    path("<int:year>/", BookingYearArchiveView.as_view(), name="booking_year_archive"),
    path(
        "<int:year>/<str:month>/",
        BookingMonthArchiveView.as_view(),
        name="archive_month",
    ),
]
