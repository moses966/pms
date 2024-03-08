from django.views.generic.dates import (
    WeekArchiveView, MonthArchiveView, YearArchiveView,
)
from django.views.generic import DetailView
from .models import Events
from django.urls import reverse

class EventWeeklyArchiveView(WeekArchiveView):
    model = Events
    queryset = Events.objects.all()
    date_field = "event_date"
    template_name = 'restaurant/weekly_events.html'
    week_format = "%W"
    allow_empty = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class EventMonthlyArchiveView(MonthArchiveView):
    model = Events
    queryset = Events.objects.all()
    date_field = "event_date"
    template_name = 'restaurant/monthly_events.html'
    allow_empty = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class EventYearlyArchiveView(YearArchiveView):
    model = Events
    queryset = Events.objects.all()
    date_field = "event_date"
    template_name = 'restaurant/yearly_events.html'
    make_object_list = True
    allow_empty = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')
        return context

class EventDetailView(DetailView):
    model = Events
    template_name = 'restaurant/event.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['home_url'] = reverse('home')
        return context

