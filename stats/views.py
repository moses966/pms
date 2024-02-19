from django.db.models import Q
from django.views.generic import ListView, DetailView
from hotel.models import Room, Category
from house_keeping.models import CleanRoom, HousekeepingTask
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rooms = context['rooms']
        room_cleaned_data = {}
        for room in rooms:
            try:
                clean_room = CleanRoom.objects.get(room=room)
                room_cleaned_data[room.pk] = clean_room.last_cleaned.strftime('%Y-%m-%d %H:%M:%S') if clean_room.last_cleaned else "Not Sure!"
            except CleanRoom.DoesNotExist:
                room_cleaned_data[room.pk] = "Not Sure!"
        context['room_cleaned_data'] = room_cleaned_data
        return context
    
class RoomDetailView(DetailView):
    model = Room
    template_name = 'stats/room_details.html'
    context_object_name = 'room_details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = context['room_details']
        try:
            clean_room = CleanRoom.objects.get(room=room)
            context['last_cleaned'] = clean_room.last_cleaned.strftime('%Y-%m-%d %H:%M:%S') if clean_room.last_cleaned else "Not Sure!"
        except CleanRoom.DoesNotExist:
            context['last_cleaned'] = "Not Sure!"
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()
        housekeeping_task = HousekeepingTask.objects.filter(room_number=room).first()
        context['task_status'] = housekeeping_task.task_status if housekeeping_task else None
        return context


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
class CleaningTasksListView(ListView):
    model = HousekeepingTask
    template_name = 'stats/cleaning_tasks.html'
    context_object_name = 'cleaning_tasks'

class CategoryListView(ListView):
    model = Category
    template_name = 'stats/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'stats/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        # Fetch all rooms associated with the category
        rooms = category.room_set.all()  # Assuming the related_name is 'room_set' in Category model
        context['rooms'] = rooms
        return context

class CleanRoomListView(ListView):
    model = CleanRoom
    template_name = 'stats/clean_rooms.html'
    context_object_name = 'clean_rooms'