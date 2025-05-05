from django.test import TestCase
from django.utils import timezone
from hsabackend.models.organization import Organization
from hsabackend.models.job import Job
from hsabackend.models.booking import Booking

class BookingModelTest(APITestCase):
    def test_booking_date_property(self):
        """Test that the booking_date property returns the correct date."""
        start_time = timezone.now()
        booking = Booking(
            event_name="Test Event",
            start_time=start_time,
            end_time=start_time + timezone.timedelta(hours=1),
            booking_type="job",
            status="pending",
            organization=Organization(),
            job=Job()
        )
        self.assertEqual(booking.booking_date, start_time.date())

    def test_duration_property(self):
        """Test that the duration property returns the correct duration in minutes."""
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1, minutes=30)  # 90 minutes
        booking = Booking(
            event_name="Test Event",
            start_time=start_time,
            end_time=end_time,
            booking_type="job",
            status="accepted",
            organization=Organization(),
            job=Job()
        )
        self.assertEqual(booking.duration, 90)
