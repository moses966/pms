from typing import Any
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.generic.dates import (
    WeekArchiveView, 
    DayArchiveView, YearArchiveView, MonthArchiveView
)
from django.utils import timezone
from datetime import date, datetime
from hotel.models import Booking
from django.urls import reverse
from django.http import Http404

class BookingDayArchiveView(DayArchiveView):
    model = Booking
    queryset = Booking.objects.all()
    date_field = "booking_date"
    template_name = 'booking_archives/booking_daily_archives.html'
    allow_empty = True
    allow_future = True

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(guest_profile__full_name__icontains=query) |
                Q(booking_number__icontains=query)
            )
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

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(guest_profile__full_name__icontains=query) |
                Q(booking_number__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context
class BookingYearArchiveView(YearArchiveView):
    model = Booking
    template_name = 'booking_archives/yearly_archives.html'
    queryset = Booking.objects.all()
    date_field = "booking_date"
    make_object_list = True
    allow_empty = True
    allow_future = True

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(guest_profile__full_name__icontains=query) |
                Q(booking_number__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class BookingMonthArchiveView(MonthArchiveView):
    model = Booking
    queryset = Booking.objects.all()
    date_field = "booking_date"
    template_name = 'booking_archives/booking_month_archive.html'
    allow_future = True
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
