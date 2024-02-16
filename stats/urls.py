# project/urls.py
from django.urls import path
from .views import RoomStatsView

urlpatterns = [
    # Other URL patterns
    path('room-stats/', RoomStatsView.as_view(), name='room_stats'),
]
