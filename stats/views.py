# stats/views.py
from django.views.generic import ListView
from hotel.models import Room

class RoomStatsView(ListView):
    model = Room
    template_name = 'stats/room_stats.html'
    context_object_name = 'rooms'
