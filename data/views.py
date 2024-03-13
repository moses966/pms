from rest_framework import generics
from darsh_board.models import MonthlyGuestStatistics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    MonthlyGuestStatisticsSerializer, GenderStatisticsSerializer
)

'''DRF View
'''
class MonthlyBookingStatisticsList(generics.ListAPIView):
    queryset = MonthlyGuestStatistics.objects.all()
    serializer_class = MonthlyGuestStatisticsSerializer

class GenderStatisticsAPIView(APIView):
    def get(self, request):
        serializer = GenderStatisticsSerializer(data=request.query_params)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

