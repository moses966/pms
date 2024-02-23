from django.urls import path
from .views import (
    ReservationDetailView, ReserveYearArchiveView,
    ReserveMonthArchiveView,
    ReserveYearArchiveView,
    ReserveWeekArchiveView,
    ReserveDayArchiveView,
)

urlpatterns = [
    path('reservation/<int:year>/<int:month>/<int:pk>/', ReservationDetailView.as_view(), name='reservation_detail'),
    path(
        "<int:year>/week/<int:week>/",
        ReserveWeekArchiveView.as_view(),
        name="archive_week_reservation",
    ),
    path(
        "<int:year>/<str:month>/<int:day>/",
        ReserveDayArchiveView.as_view(),
        name="archive_day_reservation",
    ),
    path("<int:year>/", ReserveYearArchiveView.as_view(), name="reservation_year_archive"),
    path(
        "<int:year>/<str:month>/",
        ReserveMonthArchiveView.as_view(),
        name="archive_month_reservation",
    ),
]
