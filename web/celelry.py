import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery('web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-cache': {
        'task': 'dashboard.tasks.update_cache',
        'schedule': 60.0,  # run every 60 seconds
    },
}