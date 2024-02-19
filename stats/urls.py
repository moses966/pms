# project/urls.py
from django.urls import path
from .views import (
    RoomStatsView, DepartmentDetailView,
    BaseUserDetailView, DepartmentListView,
    UserListView, RoomDetailView
)

urlpatterns = [
    path('rooms/', RoomStatsView.as_view(), name='room_stats'), # URL to rooms list view
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'), # URL to room dtails
    path('users/', UserListView.as_view(), name='user_list'), # URL to users list view
    path('users/<int:pk>/', BaseUserDetailView.as_view(), name='base_user_detail'), # URL to user details
    path('departments/', DepartmentListView.as_view(), name='department_list'), # URL to departments list view
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department_detail'), # URL to User details
]