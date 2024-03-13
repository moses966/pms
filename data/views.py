from rest_framework import generics
from .serializers import MonthlyGuestStatisticsSerializer
from darsh_board.models import MonthlyGuestStatistics

'''DRF View
'''
class MonthlyBookingStatisticsList(generics.ListAPIView):
    queryset = MonthlyGuestStatistics.objects.all()
    serializer_class = MonthlyGuestStatisticsSerializer

