from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.generic.dates import DayArchiveView
from hotel.models import Room, Category
from house_keeping.models import CleanRoom, HousekeepingTask
from management.models import User, CustomGroup
from management.customs import Departments
from django.urls import reverse

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
        context['home_url'] = reverse('home')
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
        context['home_url'] = reverse('home')
        return context


class UserListView(ListView):
    model = User
    template_name = 'stats/user.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class BaseUserDetailView(DetailView):
    model = User
    template_name = 'stats/baseuser.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class DepartmentListView(ListView):
    model = CustomGroup
    template_name = 'stats/department_list.html'
    context_object_name = 'departments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class DepartmentDetailView(DetailView):
    model = Departments
    template_name = 'stats/department_detail.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.object
        context['users'] = department.customgroup.users.all()
        context['home_url'] = reverse('home') 
        return context
    
class DailyCleaningTasksView(DayArchiveView):
    model = HousekeepingTask
    queryset = HousekeepingTask.objects.all()
    date_field = "creation_date"
    template_name = 'stats/cleaning_tasks.html'
    allow_future = True
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context
    
'''class CleaningTasksListView(ListView):
    model = HousekeepingTask
    template_name = 'stats/cleaning_tasks.html'
    context_object_name = 'cleaning_tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context'''

class CategoryListView(ListView):
    model = Category
    template_name = 'stats/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class CleaningTaskDetailView(DetailView):
    model = HousekeepingTask
    template_name = 'stats/cleaning_task_details.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['home_url'] = reverse('home')
        return context

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
        context['home_url'] = reverse('home')
        return context

class CleanRoomListView(ListView):
    model = CleanRoom
    template_name = 'stats/clean_rooms.html'
    context_object_name = 'clean_rooms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context