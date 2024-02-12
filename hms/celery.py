import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')

app = Celery('hms')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from hotel.tasks import check_reservation_deadline
    # Execute every minute
    sender.add_periodic_task(crontab(minute='*/2'), check_reservation_deadline.s())

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from ryt.tasks import subtract_one_periodically

    # Run the subtract_one_periodically task every minute
    sender.add_periodic_task(crontab(minute='*'), subtract_one_periodically.s())

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from ryt.tasks import add_one_periodically

    # Run the add_one_periodically task every minute
    sender.add_periodic_task(add_one_periodically.s())
