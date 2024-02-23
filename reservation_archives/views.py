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
from hotel.models import Reservation
from django.urls import reverse
from django.http import Http404

class ReserveDayArchiveView(DayArchiveView):
    model = Reservation
    queryset = Reservation.objects.all()
    date_field = "reservation_date"
    template_name = 'reservation_archives/daily_reservation_archives.html'
    allow_empty = True
    allow_future = True

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(Reservation_number__icontains=query) |
                Q(guest_name__icontains=query) |
                Q(status__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context
    
class ReserveWeekArchiveView(WeekArchiveView):
    queryset = Reservation.objects.all()
    date_field = "reservation_date"
    template_name = 'reservation_archives/weekly_reservation_archives.html'
    week_format = "%W"
    allow_empty = True
    allow_future = True

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(Reservation_number__icontains=query) |
                Q(guest_name__icontains=query) |
                Q(status__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context
    
class ReserveYearArchiveView(YearArchiveView):
    model = Reservation
    template_name = 'reservation_archives/yearly_reservation_archives.html'
    queryset = Reservation.objects.all()
    date_field = "reservation_date"
    make_object_list = True
    allow_empty = True
    allow_future = True

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(Reservation_number__icontains=query) |
                Q(guest_name__icontains=query) |
                Q(status__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class ReserveMonthArchiveView(MonthArchiveView):
    model = Reservation
    queryset = Reservation.objects.all()
    date_field = "reservation_date"
    template_name = 'reservation_archives/monthly_reservation_archives.html'
    allow_future = True
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservation_archives/reservation_details.html'
    context_object_name = 'reservation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['home_url'] = reverse('home')
        return context