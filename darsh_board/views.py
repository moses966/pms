from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from datetime import date
from hotel.models import Booking, PaymentInformation
from django.shortcuts import get_object_or_404
from .models import (
    MonthlyGuestStatistics, DailyBookingStatistics,
    DailyGuestStatistics
)

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'darsh_board/home3.html'

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

        """context for fetching daily bookings
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
        return context

class InvoiceDetailView(DetailView):
    model = Booking
    template_name = 'darsh_board/invoice.html'
    context_object_name = 'booking'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = self.get_object()
        payment_info = get_object_or_404(PaymentInformation, booking_info=booking)
        # Retrieve food or drinks for the booking
        food_or_drinks = booking.booking_food.all()
        # Retrieve other services for the booking
        other_services = booking.booking_service.all()
        # Retrieve the last other service for the booking
        last_other_service = booking.booking_service.last()
        # Retrieve the last food or drink for the booking
        last_food = booking.booking_food.last()
        # Calculate total bill
        total_bill = booking.calculate_total_bill()

        context['total_bill'] = total_bill
        context['payment_info'] = payment_info
        context['food_or_drinks'] = food_or_drinks
        context['other_services'] = other_services
        context['last_other_service'] = last_other_service
        context['last_food'] = last_food
        return context

