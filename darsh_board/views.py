from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from datetime import date
from .models import (
    MonthlyGuestStatistics, DailyBookingStatistics,
    DailyGuestStatistics
)

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'darsh_board/home.html'

    def get_context_data(self, **kwargs):
        """context for fetching monthly bookings and guest statistics
        """
        context = super().get_context_data(**kwargs)
        # Call the update_statistics method to ensure statistics are up-to-date
        MonthlyGuestStatistics.update_statistics()
        # Retrieve the latest statistics
        monthly_statistics = MonthlyGuestStatistics.objects.latest('month_year')
        # Pass the statistics to the template context
        context['monthly_statistics'] = monthly_statistics
        
        """context for fetching dail bookings
        """
       # Call the update_statistics method to ensure statistics are up-to-date
        DailyBookingStatistics.update_statistics()
        # Retrieve the daily booking statistics for the current date
        daily_booking_statistics = DailyBookingStatistics.objects.filter(date=date.today()).first()
        # Pass the statistic to the template context
        context['daily_booking_statistics'] = daily_booking_statistics

        """context for fetching daily checkins
        """
        # Call the update_statistics method to ensure statistics are up-to-date
        DailyGuestStatistics.update_statistics()
        # Retrieve the daily guest statistics for the current date
        daily_guest_statistics = DailyGuestStatistics.objects.filter(date=date.today()).first()
        # Pass the statistic to the template context
        context['daily_guest_statistics'] = daily_guest_statistics
        """accesing total bill
        """
        booking = self.get_object()
        context['total_bill'] = booking.total_bill
        return context
