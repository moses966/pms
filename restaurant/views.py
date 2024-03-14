from django.views.generic.dates import (
    WeekArchiveView, MonthArchiveView, YearArchiveView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView
from .models import Events
from django.urls import reverse
from django.shortcuts import render

class EventWeeklyArchiveView(LoginRequiredMixin, PermissionRequiredMixin, WeekArchiveView):
    model = Events
    queryset = Events.objects.all()
    date_field = "event_date"
    template_name = 'restaurant/weekly_events.html'
    week_format = "%W"
    allow_empty = True
    allow_future = True
    permission_required = 'restaurant.view_events'

    def handle_no_permission(self):
        return render(self.request, 'errors/403.html', status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class EventMonthlyArchiveView(LoginRequiredMixin, PermissionRequiredMixin, MonthArchiveView):
    model = Events
    queryset = Events.objects.all()
    date_field = "event_date"
    template_name = 'restaurant/monthly_events.html'
    allow_empty = True
    allow_future = True
    permission_required = 'restaurant.view_events'

    def handle_no_permission(self):
        return render(self.request, 'errors/403.html', status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class EventYearlyArchiveView(LoginRequiredMixin, PermissionRequiredMixin, YearArchiveView):
    model = Events
    queryset = Events.objects.all()
    date_field = "event_date"
    template_name = 'restaurant/yearly_events.html'
    make_object_list = True
    allow_empty = True
    allow_future = True
    permission_required = 'restaurant.view_events'

    def handle_no_permission(self):
        return render(self.request, 'errors/403.html', status=403)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class EventDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Events
    template_name = 'restaurant/event.html'
    context_object_name = 'events'
    permission_required = 'restaurant.view_events'

    def handle_no_permission(self):
        return render(self.request, 'errors/403.html', status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['home_url'] = reverse('home')
        return context

