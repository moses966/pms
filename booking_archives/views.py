from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView, WeekArchiveView
from django.utils import timezone
from datetime import date, datetime
from hotel.models import Booking
from django.urls import reverse
from django.http import Http404

class CustomTodayArchiveView(ArchiveIndexView):
    """
    Custom view to display a list of bookings made today.
    """
    model = Booking
    date_field = "booking_date"
    allow_empty = True
    template_name = "booking_archives/custom_today_archive.html"
    context_object_name = 'bookings'

    def get_queryset(self):
        today = timezone.now().date()
        queryset = super().get_queryset().filter(booking_date=today)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context
    
class BookingWeekArchiveView(WeekArchiveView):
    queryset = Booking.objects.all()
    date_field = "booking_date"
    template_name = 'booking_archives/booking_weekly_archives.html'
    week_format = "%W"
    allow_empty = True
    allow_future = True
    #context_object_name = 'weekly_bookings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class BookingYearArchiveView(TemplateView):
    """
    Displays a list of yearly archives for bookings.
    Inherits:
        TemplateView
    Attributes:
        template_name (str): Name of the template for yearly archives ('booking_archives/booking_year_archive.html').
        context_object_name (str): Name of the context variable for yearly archives ('yearly_archives').
        start_year (int): Starting year for the archives (2023).
    Functionality:
        Renders the yearly archives template.
        Provides a range of years in the context.
    """
    template_name = 'booking_archives/booking_year_archive.html'
    context_object_name = 'yearly_archives'
    start_year = 2023
    
    def get_context_data(self, **kwargs):
        """
        Adds a range of years to the context.
        Functionality:
            Retrieves the current year.
            Constructs a range of years from the start year to the current year.
            Adds the range of years to the context.
        """
        context = super().get_context_data(**kwargs)
        current_year = timezone.now().year
        context['years'] = range(self.start_year, current_year + 1)
        context['home_url'] = reverse('home')
        return context

class BookingMonthArchiveView(ListView):
    """
    Displays monthly archives for bookings.
    Inherits:
        ListView
    Attributes:
        template_name (str): Name of the template for monthly archives ('booking_archives/booking_month_archive.html').
        context_object_name (str): Name of the context variable for monthly archives ('monthly_archives').
        queryset (QuerySet): All bookings.
    Functionality:
        Renders the monthly archives template.
        Filters bookings based on the provided year and month.
        Provides monthly archives in the context.
    """
    template_name = 'booking_archives/booking_month_archive.html'
    context_object_name = 'monthly_archives'
    queryset = Booking.objects.all()  # Queryset including all bookings

    def get(self, request, *args, **kwargs):
        """
        Retrieves the year and month from the URL parameters.
        Functionality:
            Extracts the year from the URL.
            Extracts the month from the URL or defaults to the current month.
            Calls the parent get method.
        """
        self.year = int(kwargs.get('year'))
        self.month = int(request.GET.get('month', timezone.now().month))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filters the queryset based on the year and month.
        Functionality:
            Filters the bookings based on the provided year and month.
            Orders the bookings by booking date.
            Returns the filtered queryset.
        """
        return self.queryset.filter(
            booking_date__year=self.year,
            booking_date__month=self.month
        ).order_by('-booking_date')

    def get_context_data(self, **kwargs):
        """
        Adds the year, month, and monthly archives to the context.
        Functionality:
            Adds the year and month to the context.
            Constructs a list of monthly archives containing bookings for each month.
            Adds the list of monthly archives to the context.
        """
        context = super().get_context_data(**kwargs)
        context['year'] = self.year
        context['month'] = self.month
        
        monthly_archives = []
        for month in range(1, 13):
            monthly_bookings = self.queryset.filter(
                booking_date__year=self.year,
                booking_date__month=month
            ).order_by('-booking_date')
            monthly_archive = {
                'month': month,
                'bookings': monthly_bookings
            }
            monthly_archives.append(monthly_archive)
        
        context['monthly_archives'] = monthly_archives
        context['home_url'] = reverse('home')
        return context

class BookingDetailView(DetailView):
    """
    Displays details of a specific booking.
    Inherits:
        DetailView

    Attributes:
        model: Booking
        template_name (str): Name of the template for booking details ('booking_archives/booking_details.html').
        context_object_name (str): Name of the context variable for the booking ('booking').
    Functionality:
        Renders the booking details template.
        Retrieves the year and month from the URL parameters.
        Adds the year and month to the context.
    """
    model = Booking
    template_name = 'booking_archives/booking_details.html'
    context_object_name = 'booking'

    def get_context_data(self, **kwargs):
        """
        Adds the year and month to the context.
        Functionality:
            Retrieves the year and month from the URL parameters.
            Adds the year and month to the context.
        """
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['home_url'] = reverse('home')
        return context
