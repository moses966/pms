# project/urls.py
from django.urls import path
from .views import (
    RoomStatsView, DepartmentDetailView,
    BaseUserDetailView, DepartmentListView,
    UserListView,
)

urlpatterns = [
    path('room-stats/', RoomStatsView.as_view(), name='room_stats'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('baseuser/<int:pk>/', BaseUserDetailView.as_view(), name='base_user_detail'),
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('department/<int:pk>/', DepartmentDetailView.as_view(), name='department_detail'),
]