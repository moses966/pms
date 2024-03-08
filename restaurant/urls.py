from django.urls import path
from .views import (
    EventWeeklyArchiveView, EventMonthlyArchiveView, EventYearlyArchiveView, EventDetailView,
)

urlpatterns = [
    path('<int:year>/week/<int:week>/', EventWeeklyArchiveView.as_view(), name='weekly_archive'),
    path('<int:year>/<str:month>/', EventMonthlyArchiveView.as_view(), name='monthly_archive'),
    path('<int:year>/', EventYearlyArchiveView.as_view(), name='yearly_archive'),
    path('<int:year>/<int:month>/<int:pk>/', EventDetailView.as_view(), name='event'),
]
