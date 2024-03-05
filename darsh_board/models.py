from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from hotel.models import Booking, Guest

class MonthlyGuestStatistics(models.Model):
    month_year = models.DateField(unique=True)
    total_guests = models.IntegerField(default=0)
    male_guests = models.IntegerField(default=0)
    female_guests = models.IntegerField(default=0)

    @classmethod
    def update_statistics(cls):
        today = timezone.now()
        first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day_of_month = first_day_of_month + relativedelta(months=1, days=-1)

        # Filter bookings within the current month
        monthly_bookings = Booking.objects.filter(check_in_date__gte=first_day_of_month,
                                                   check_in_date__lte=last_day_of_month)

        # Initialize counters
        total_guests = 0
        male_guests = 0
        female_guests = 0

        # Iterate through each booking and count guests
        for booking in monthly_bookings:
            try:
                guest = Guest.objects.get(guest_profile=booking)
                total_guests += 1
                if guest.gender.gender_choices.lower() == 'male':
                    male_guests += 1
                elif guest.gender.gender_choices.lower() == 'female':
                    female_guests += 1
            except Guest.DoesNotExist:
                pass

        # Create or update the monthly statistics
        month_year = first_day_of_month.replace(day=1)
        monthly_statistics, created = cls.objects.get_or_create(month_year=month_year)
        monthly_statistics.total_guests = total_guests
        monthly_statistics.male_guests = male_guests
        monthly_statistics.female_guests = female_guests
        monthly_statistics.save()

    def __str__(self):
        return self.month_year.strftime('%B %Y')
    
class DailyBookingStatistics(models.Model):
    date = models.DateField(unique=True)
    num_bookings = models.IntegerField(default=0)

    @classmethod
    def update_statistics(cls):
        # Get today's date
        today = timezone.now().date()

        # Retrieve bookings for today
        bookings_today = Booking.objects.filter(booking_date=today)

        # Count the number of bookings for today
        num_bookings_today = bookings_today.count()

        # Get or create DailyBookingStatistics object for today
        daily_statistics, created = cls.objects.get_or_create(date=today)

        # Update the number of bookings for today
        daily_statistics.num_bookings = num_bookings_today
        daily_statistics.save()

    def __str__(self):
        return str(self.date)
class DailyGuestStatistics(models.Model):
    date = models.DateField(unique=True)
    num_guests = models.IntegerField(default=0)

    @classmethod
    def update_statistics(cls):
        # Get today's date
        today = timezone.now().date()

        # Retrieve bookings with check-in dates for today
        bookings_today = Booking.objects.filter(check_in_date__date=today)

        # Count the number of guests for today
        num_guests_today = bookings_today.count()

        # Get or create DailyGuestStatistics object for today
        daily_statistics, created = cls.objects.get_or_create(date=today)

        # Update the number of guests for today
        daily_statistics.num_guests = num_guests_today
        daily_statistics.save()

    def __str__(self):
        return str(self.date)
