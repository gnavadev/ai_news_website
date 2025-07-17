import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'absurd_news.settings')
app = Celery('absurd_news')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
