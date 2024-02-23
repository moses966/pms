# project/urls.py
from django.urls import path
from .views import (
    RoomStatsView, DepartmentDetailView,
    BaseUserDetailView, DepartmentListView,
    UserListView, RoomDetailView, DailyCleaningTasksView,
    CategoryDetailView, CategoryListView, CleanRoomListView,
    CleaningTaskDetailView,
)

urlpatterns = [
    path('rooms/', RoomStatsView.as_view(), name='room_stats'), # URL to rooms list view
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'), # URL to room dtails
    path('cleaning-tasks/<int:year>/<str:month>/<int:day>/', DailyCleaningTasksView.as_view(), name='cleaning_task_archives'), # URL to rooms cleaning tasks
    path('cleaning-task/<int:year>/<int:month>/<int:pk>/', CleaningTaskDetailView.as_view(), name='cleaning_task_detail'),
    path('users/', UserListView.as_view(), name='user_list'), # URL to users list view
    path('users/<int:pk>/', BaseUserDetailView.as_view(), name='base_user_detail'), # URL to user details
    path('departments/', DepartmentListView.as_view(), name='department_list'), # URL to departments list view
    path('rooms/room-category/', CategoryListView.as_view(), name='category_list'), # URL to Categories list view
    path('rooms/room-category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'), # URL to Category detail view
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department_detail'), # URL to User details
    path('rooms/clean-rooms/', CleanRoomListView.as_view(), name='clean_rooms_list')
]