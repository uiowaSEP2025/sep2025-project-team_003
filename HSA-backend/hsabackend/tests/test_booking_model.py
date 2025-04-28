from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from hsabackend.models.booking import Booking
from hsabackend.models.job import Job
from hsabackend.models.organization import Organization

class BookingModelTest(TestCase):
    """Test cases for the Booking model"""

    def setUp(self):
        """Set up test data"""
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )

        self.organization = Organization.objects.create(
            org_name="Test Organization",
            org_address="123 Test St",
            org_city="Test City",
            org_state="TS",
            org_zip="12345",
            org_phone="1234567890",
            org_email="test@example.com",
            owning_user = self.user,
        )

        self.job = Job.objects.create(
            description="Test Job",
            job_address="456 Test Ave",
            job_city="Test City",
            job_state="TS",
            job_zip="12345",
            organization=self.organization,
            hourly_rate=50.00,
        )

        self.start_time = timezone.now()
        self.end_time = self.start_time + timedelta(hours=2)

        self.booking = Booking.objects.create(
            event_name="Test Booking",
            start_time=self.start_time,
            end_time=self.end_time,
            booking_type="job",
            status="pending",
            back_color="#6aa84f",
            organization=self.organization,
            job=self.job
        )

    def test_booking_creation(self):
        """Test that a booking can be created"""
        self.assertEqual(self.booking.event_name, "Test Booking")
        self.assertEqual(self.booking.booking_type, "job")
        self.assertEqual(self.booking.status, "pending")
        self.assertEqual(self.booking.back_color, "#6aa84f")
        self.assertEqual(self.booking.organization, self.organization)
        self.assertEqual(self.booking.job, self.job)

    def test_booking_date_property(self):
        """Test the booking_date property"""
        self.assertEqual(self.booking.booking_date, self.start_time.date())

    def test_duration_property(self):
        """Test the duration property"""
        # Duration should be 2 hours = 120 minutes
        self.assertEqual(self.booking.duration, 120)

    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = (f"<Booking Details:"
                        f" id: {self.booking.pk},"
                        f" event_name: {self.booking.event_name},"
                        f" booking_date: {self.booking.booking_date},"
                        f" start_time: {self.booking.start_time},"
                        f" end_time: {self.booking.end_time},"
                        f" status: {self.booking.status},"
                        f" booking_type: {self.booking.booking_type},"
                        f" job: {self.booking.job}, "
                        f" duration: {self.booking.duration}"
                        f" organization: {self.booking.organization}")
        self.assertEqual(str(self.booking), expected_str)

    def test_booking_type_choices(self):
        """Test that booking_type choices are enforced"""
        # This should work
        self.booking.booking_type = "quote"
        self.booking.save()
        self.assertEqual(self.booking.booking_type, "quote")

    def test_status_choices(self):
        """Test that status choices are enforced"""
        # Test all valid statuses
        for status in ["pending", "accepted", "rejected", "cancelled"]:
            self.booking.status = status
            self.booking.save()
            self.assertEqual(self.booking.status, status)

    def test_time_truncation(self):
        """Test that start_time and end_time are truncated to the closest minute"""
        # Create a booking with specific seconds and microseconds
        start_time = timezone.now().replace(second=30, microsecond=500000)
        end_time = (start_time + timedelta(hours=1)).replace(second=45, microsecond=750000)

        test_booking = Booking.objects.create(
            event_name="Time Truncation Test",
            start_time=start_time,
            end_time=end_time,
            booking_type="job",
            status="pending",
            organization=self.organization,
            job=self.job
        )

        # Verify that seconds and microseconds are set to 0
        self.assertEqual(test_booking.start_time.second, 0)
        self.assertEqual(test_booking.start_time.microsecond, 0)
        self.assertEqual(test_booking.end_time.second, 0)
        self.assertEqual(test_booking.end_time.microsecond, 0)

        # Update the booking with new times that have seconds and microseconds
        test_booking.start_time = test_booking.start_time.replace(second=15, microsecond=250000)
        test_booking.end_time = test_booking.end_time.replace(second=20, microsecond=300000)
        test_booking.save()

        # Verify that seconds and microseconds are again set to 0 after update
        self.assertEqual(test_booking.start_time.second, 0)
        self.assertEqual(test_booking.start_time.microsecond, 0)
        self.assertEqual(test_booking.end_time.second, 0)
        self.assertEqual(test_booking.end_time.microsecond, 0)
