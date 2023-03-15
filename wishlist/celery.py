from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wishlist.settings')


app = Celery('wishlist')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
