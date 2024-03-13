from rest_framework import serializers
from django.db.models import Count
from calendar import month_abbr
from hotel.models import Booking, Guest
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import date
from calendar import month_abbr

class MonthlyGuestStatisticsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        # Get the current year
        current_year = date.today().year
        
        # Create a dictionary to store total bookings for each month
        bookings_data = {month_abbr[i]: 0 for i in range(1, 13)}

        # Query the database to get total bookings for each month of the current year
        bookings_by_month = Booking.objects.filter(booking_date__year=current_year).annotate(
            month=TruncMonth('booking_date')
        ).values('month').annotate(
            total_bookings=Count('id')
        ).order_by('month')

        # Update the bookings_data dictionary with the total bookings for each month
        for month_info in bookings_by_month:
            month_abbr_key = month_abbr[month_info['month'].month]
            bookings_data[month_abbr_key] = month_info['total_bookings']

        return bookings_data
    
class GenderStatisticsSerializer(serializers.Serializer):
    year = serializers.IntegerField()

    def to_representation(self, instance):
        year = self.validated_data.get('year', None)
        if year is None:
            return {'error': 'Year not provided'}

        # Calculate total male and female guests for the given year
        male_guests_count = Guest.objects.filter(guest_profile__check_in_date__year=year, gender__gender_choices__iexact='male').count()
        female_guests_count = Guest.objects.filter(guest_profile__check_in_date__year=year, gender__gender_choices__iexact='female').count()

        return {
            'year': year,
            'male_guests_count': male_guests_count,
            'female_guests_count': female_guests_count
        }
