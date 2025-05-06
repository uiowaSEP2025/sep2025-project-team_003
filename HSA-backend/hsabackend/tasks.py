# hsabackend/tasks.py
import datetime
import logging

from celery import shared_task
from django.utils import timezone

from hsabackend.models.booking import Booking

logger = logging.getLogger(__name__)

@shared_task
def check_upcoming_bookings():
    """
    Finds all bookings starting between now and now+5min.
    """
    now = timezone.now()
    window = now + datetime.timedelta(minutes=5)

    qs = Booking.objects.filter(
        start_time__gte=now,
        start_time__lte=window,
    )

    if not qs.exists():
        logger.info("No bookings in the next 5 minutes.")
        return

    for booking in qs:
        # replace this with whatever you actually want to do
        logger.info(
            f"🔔 Booking #{booking.pk} starts at {booking.start_time.isoformat()}"
        )
        # e.g. booking.notify_user(), or send emails, etc.
