import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_quotes.settings.base')
app = Celery('daily_quotes')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Add this line to use Celery Beat as the periodic task scheduler
app.conf.beat_scheduler = "django_celery_beat.schedulers.DatabaseScheduler"


app.autodiscover_tasks()
