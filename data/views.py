from rest_framework import generics, permissions
from darsh_board.models import MonthlyGuestStatistics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from .serializers import (
    MonthlyGuestStatisticsSerializer, GenderStatisticsSerializer
)

'''permissions'''
class CustomIsAdminUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        return False

'''DRF View
'''
class MonthlyBookingStatisticsList(generics.ListAPIView):
    queryset = MonthlyGuestStatistics.objects.all()
    serializer_class = MonthlyGuestStatisticsSerializer
    permission_classes = [CustomIsAdminUser]

class GenderStatisticsAPIView(APIView):
    permission_classes = [CustomIsAdminUser]
    def get(self, request):
        serializer = GenderStatisticsSerializer(data=request.query_params)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

