**TASK SCHEDULING**  
*-django-celery-beat, django-celery-results, rabbitMQ*
1. Install a broker: `sudo apt-get install rabbitmq-server`
2. Then, install celery, django-celery-beat, django-celery-results:
3. `python -m pip install celery django-celery-beat django-celery-results`
4. Then add the following to settings.py:
5. ```python
   # ..... other code
   INSTALLED_APPS = [
        # other installed apps
       'django-celery-beat',
       'django-celery-results',
       # other installed apps
   ]
   # save Celery task results in Django's database
   CELERY_RESULT_BACKEND = "django-db"
   # this allows you to schedule items in the Django admin.
   CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

   BROKER_URL = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')

   # Set this to True to retain the existing behavior for retrying connections on startup
   CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
   ```
6. In your root directory, create a file called `celery.py`
7. ```python
   import os
   from celery import Celery
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
   ```
7. In the __init__py file of the root directory, add the following code:
8. ```python
   # This will make sure the app is always imported when
   # Django starts so that shared_task will use this app.
   from .celery import app as celery_app

   __all__ = ('celery_app',)
   ```
9. Within your app, create a task.py file:
10. ```python
    # In your tasks.py file

    from celery import shared_task
    from django.utils import timezone
    from .models import Remove, PileUp

    @shared_task
    def subtract_one_periodically():
        # Retrieve the instance of Remove from the database
        remove_instance = Remove.objects.first()

        if remove_instance:
           # Subtract 1 from the number field
           remove_instance.number -= 1
           remove_instance.save()

    @shared_task(name='Add_one_to_number')
    def add_one_periodically():
        # Retrieve the instance of Remove from the database
        add_instance = PileUp.objects.first()

        if add_instance:
           # Subtract 1 from the number field
           add_instance.number += 1
           add_instance.save()

    ```
11. Then, our full code in celery.py shall look like this:
12. ```python
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
        from ryt.tasks import subtract_one_periodically

       # Run the subtract_one_periodically task every minute
       sender.add_periodic_task(crontab(minute='*'), subtract_one_periodically.s())

    @app.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        from ryt.tasks import add_one_periodically

        # Run the add_one_periodically task every minute
        sender.add_periodic_task(add_one_periodically.s())

    ```
13. **ADMIN**
14. Remember, we added a setting to allow our schedules to be performed in the django-admin:
15. ![image](https://github.com/moses966/pms/assets/127250388/0fe371b9-9aa5-4611-91f7-c6fc3dfc9321)
16. We can navigate to either, crontab, interval, solar or clock to set up rules for the scheduling of our application.
17. For example, such a setting below will ensure that the program run 5 minutes every after an hour everyday.
    ![image](https://github.com/moses966/pms/assets/127250388/3f97e231-5f0f-4bef-a4b1-88ff4525840e)  
19. And an interval setting below will ensure that the program runs every after 4 minutes:
   ![image](https://github.com/moses966/pms/assets/127250388/1d7b6cb6-db05-4439-97cf-9a40a9a4604f)


