import pytest
from unittest import mock
from django.utils import timezone
from datetime import timedelta

from hsabackend.tasks import check_upcoming_bookings
from hsabackend.models import Booking, Job, Customer, Contractor, JobContractor


@pytest.mark.django_db
@mock.patch("hsabackend.tasks.EmailMultiAlternatives.send")
@mock.patch("hsabackend.tasks.timezone")
def test_check_upcoming_bookings_sends_emails(mock_timezone, mock_send):
    now = timezone.now()
    mock_timezone.localtime.return_value = now
    mock_timezone.now.return_value = now

    # Setup data
    customer = Customer.objects.create(
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com"
    )
    contractor = Contractor.objects.create(
        first_name="Bob",
        email="bob@example.com"
    )
    job = Job.objects.create(customer=customer)
    booking = Booking.objects.create(
        job=job,
        event_name="Strategy Call",
        booking_type="Consultation",
        start_time=now + timedelta(minutes=5),
        end_time=now + timedelta(minutes=35),
    )
    JobContractor.objects.create(job=job, contractor=contractor)

    # Run task
    check_upcoming_bookings()

    # Should send to customer and contractor
    assert mock_send.call_count == 2
