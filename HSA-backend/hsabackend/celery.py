# project/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hsabackend.settings")
app = Celery("hsabackend")
app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks() # run our task every minute
app.conf.beat_schedule = {
    "check-upcoming-bookings": {
        "task": "hsabackend.tasks.check_upcoming_bookings",
        "schedule": crontab(minute="*"),  # every minute
    },
}

# optional: make sure times use your Django TIME_ZONE
app.conf.timezone = "UTC"
