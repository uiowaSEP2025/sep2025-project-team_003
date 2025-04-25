from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from hsabackend.models.booking import Booking
from hsabackend.models.organization import Organization
from hsabackend.models.job import Job
from django.contrib.auth.models import User

class BookingModelTest(TestCase):
    def setUp(self):
        # Create a user for the organization
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create an organization
        self.organization = Organization.objects.create(
            name='Test Organization',
            address='123 Test St',
            city='Test City',
            state='TS',
            zip_code='12345',
            phone='123-456-7890',
            email='org@example.com',
            owner=self.user
        )
        
        # Create a job
        self.job = Job.objects.create(
            name='Test Job',
            description='Test Description',
            status='pending',
            organization=self.organization
        )
        
        # Create a booking
        self.start_time = timezone.now()
        self.end_time = self.start_time + timedelta(hours=2)
        self.booking = Booking.objects.create(
            event_name='Test Booking',
            start_time=self.start_time,
            end_time=self.end_time,
            booking_type='job',
            status='pending',
            back_color='#6aa84f',
            organization=self.organization,
            job=self.job
        )
    
    def test_booking_creation(self):
        """Test that a booking can be created with the expected values"""
        self.assertEqual(self.booking.event_name, 'Test Booking')
        self.assertEqual(self.booking.start_time, self.start_time)
        self.assertEqual(self.booking.end_time, self.end_time)
        self.assertEqual(self.booking.booking_type, 'job')
        self.assertEqual(self.booking.status, 'pending')
        self.assertEqual(self.booking.back_color, '#6aa84f')
        self.assertEqual(self.booking.organization, self.organization)
        self.assertEqual(self.booking.job, self.job)
    
    def test_booking_date_property(self):
        """Test the booking_date property returns the correct date"""
        self.assertEqual(self.booking.booking_date, self.start_time.date())
    
    def test_duration_property(self):
        """Test the duration property returns the correct duration in minutes"""
        # Duration should be 2 hours = 120 minutes
        self.assertEqual(self.booking.duration, 120)
    
    def test_str_method(self):
        """Test the __str__ method returns the expected string representation"""
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
        """Test that booking_type can only be set to valid choices"""
        # Test valid choices
        self.booking.booking_type = 'job'
        self.booking.save()
        self.assertEqual(self.booking.booking_type, 'job')
        
        self.booking.booking_type = 'quote'
        self.booking.save()
        self.assertEqual(self.booking.booking_type, 'quote')
    
    def test_status_choices(self):
        """Test that status can only be set to valid choices"""
        # Test valid choices
        for status in ['pending', 'accepted', 'rejected', 'cancelled']:
            self.booking.status = status
            self.booking.save()
            self.assertEqual(self.booking.status, status)