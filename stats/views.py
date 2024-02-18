from django.db.models import Q
from django.views.generic import ListView, DetailView
from hotel.models import Room
from management.models import User, CustomGroup
from management.customs import Departments

class RoomStatsView(ListView):
    model = Room
    template_name = 'stats/room_stats.html'
    context_object_name = 'rooms'
    paginate_by = 10
    ordering = ['room_number']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the search query from the GET parameters
        query = self.request.GET.get('q')
        if query:
            # Perform search query
            queryset = queryset.filter(
                Q(name__icontains=query) 
                | Q(capacity__icontains=query)
                | Q(status__icontains=query)
                | Q(room_number__icontains=query)
            )
        return queryset
    
class RoomDetailView(DetailView):
    model = Room
    template_name = 'stats/room_details.html'
    context_object_name = 'room_details'


class UserListView(ListView):
    model = User
    template_name = 'stats/user.html'
    context_object_name = 'users'

class BaseUserDetailView(DetailView):
    model = User
    template_name = 'stats/baseuser.html'
    context_object_name = 'user'

class DepartmentListView(ListView):
    model = CustomGroup
    template_name = 'stats/department_list.html'
    context_object_name = 'departments'

class DepartmentDetailView(DetailView):
    model = Departments
    template_name = 'stats/department_detail.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.object.user_set.all()
        return context