# hsabackend/tasks.py

import datetime
import logging
import os

from celery import shared_task
from django.utils import timezone
from django.template import Template, Context
from django.core.mail import EmailMultiAlternatives

from hsabackend.models.booking import Booking

logger = logging.getLogger(__name__)

@shared_task
def check_upcoming_bookings():
    """
    Finds all bookings starting between now and now+15min,
    and emails the customer plus each contractor.
    """
    now = timezone.localtime(timezone.now())
    window = now + datetime.timedelta(minutes=15)

    logger.debug(f"Looking for bookings between {now} and {window}")

    qs = Booking.objects.filter(
        start_time__gte=now,
        start_time__lte=window,
    )

    if not qs.exists():
        logger.info("No bookings in the next 15 minutes.")
        return

    from_email = os.environ.get('EMAIL_HOST_USER', None)

    # Templates for customer
    customer_text_tpl = Template("""
Hello {{ username }},

You have a meeting scheduled our organization in less than 15 minutes.

Event: "{{ event_name }}"
Type: {{ booking_type }}
When: {{ start_time }} to {{ end_time }}

If you need to reschedule, please contact us.

""")

    customer_html_tpl = Template("""
<html>
  <body>
    <p>Hello {{ username }},</p>
    <p>You have a meeting scheduled with our organization in less than 15 minutes.</p>
    <ul>
      <li><strong>Event:</strong> {{ event_name }}</li>
      <li><strong>Type:</strong> {{ booking_type }}</li>
      <li><strong>When:</strong> {{ start_time }} to {{ end_time }}</li>
    </ul>
    <p>If you need to reschedule, please contact us.</p>
  </body>
</html>
""")

    # Templates for contractor
    contractor_text_tpl = Template("""
Hello {{ contractor_name }},

You have a meeting with customer {{ customer_name }} in less than 15 minutes.

Event: "{{ event_name }}"
Type: {{ booking_type }}
When: {{ start_time }} to {{ end_time }}

Please be on time.
""")

    contractor_html_tpl = Template("""
<html>
  <body>
    <p>Hello {{ contractor_name }},</p>
    <p>You have a meeting with customer <strong>{{ customer_name }}</strong> in less than 15 minutes.</p>
    <ul>
      <li><strong>Event:</strong> {{ event_name }}</li>
      <li><strong>Type:</strong> {{ booking_type }}</li>
      <li><strong>When:</strong> {{ start_time }} to {{ end_time }}</li>
    </ul>
    <p>Please be on time.</p>
  </body>
</html>
""")

    for booking in qs:
        # Prepare common context variables
        ctx = {
            'username': booking.job.customer.first_name,
            'customer_name': booking.job.customer.first_name + ' ' + booking.job.customer.last_name,
            'event_name': booking.event_name,
            'booking_type': booking.booking_type,
            'start_time': timezone.localtime(booking.start_time).strftime("%Y-%m-%d %H:%M"),
            'end_time': timezone.localtime(booking.end_time).strftime("%Y-%m-%d %H:%M"),
        }

        # --- Send to Customer ---
        cust_ctx = Context(ctx)
        subject = f"Upcoming Booking #{booking.pk}"
        text_content = customer_text_tpl.render(cust_ctx)
        html_content = customer_html_tpl.render(cust_ctx)
        cust_email = booking.job.customer.email

        msg = EmailMultiAlternatives(subject, text_content, from_email, [cust_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info(f"Sent upcoming‐booking email to customer {cust_email}")

        # --- Send to Contractors ---
        for jc in booking.job.jobcontractor_set.all():
            contractor = jc.contractor
            # plug in contractor‐specific context
            contractor_ctx = Context({**ctx, 'contractor_name': contractor.first_name})
            text_content = contractor_text_tpl.render(contractor_ctx)
            html_content = contractor_html_tpl.render(contractor_ctx)
            contractor_email = contractor.email

            msg = EmailMultiAlternatives(subject, text_content, from_email, [contractor_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            logger.info(f"Sent upcoming‐booking email to contractor {contractor_email}")

    logger.info("All upcoming booking notifications sent.")
