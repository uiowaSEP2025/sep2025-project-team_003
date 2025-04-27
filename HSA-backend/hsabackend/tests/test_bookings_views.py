from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
import json
from hsabackend.models.booking import Booking
from hsabackend.models.job import Job
from hsabackend.models.organization import Organization

class BookingsViewsTest(TestCase):
    """Test cases for the Bookings views"""
    
    def setUp(self):
        """Set up test data"""
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        
        # Create an organization
        self.organization = Organization.objects.create(
            org_name="Test Organization",
            org_email="test@example.com",
            org_city="Test City",
            org_state="TS",
            org_zip="12345",
            org_address="123 Test St",
            org_phone="1234567890",
            org_owner_first_name="John",
            org_owner_last_name="Doe",
            owning_user=self.user,
            is_onboarding=False,
            default_labor_rate=50.00
        )
        
        # Create a job
        self.job = Job.objects.create(
            job_status="created",
            description="Test Job Description",
            organization=self.organization,
            job_city="Test City",
            job_state="TS",
            job_zip="12345",
            job_address="456 Test Ave"
        )
        
        # Create a booking
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
        
        # Set up the API client
        self.client = APIClient()
        
        # URLs
        self.get_booking_data_url = reverse('get_booking_data')
        self.create_event_url = reverse('create_event')
        self.edit_event_url = reverse('edit_event', args=[self.booking.pk])
        self.delete_event_url = reverse('delete_event', args=[self.booking.pk])
    
    def test_get_booking_data_unauthenticated(self):
        """Test that unauthenticated users cannot get booking data"""
        response = self.client.get(self.get_booking_data_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_booking_data_authenticated(self):
        """Test that authenticated users can get booking data"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_booking_data_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertEqual(len(data['data']), 1)  # Should have one booking
    
    def test_create_event_unauthenticated(self):
        """Test that unauthenticated users cannot create events"""
        response = self.client.post(self.create_event_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_event_authenticated(self):
        """Test that authenticated users can create events"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare event data
        start_time = timezone.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=2)
        
        event_data = {
            'eventName': 'New Test Booking',
            'startTime': start_time.isoformat(),
            'endTime': end_time.isoformat(),
            'bookingType': 'job',
            'backColor': '#6aa84f',
            'jobID': self.job.pk
        }
        
        response = self.client.post(self.create_event_url, event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the booking was created
        self.assertEqual(Booking.objects.count(), 2)
        new_booking = Booking.objects.latest('id')
        self.assertEqual(new_booking.event_name, 'New Test Booking')
    
    def test_create_event_invalid_data(self):
        """Test that events cannot be created with invalid data"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare invalid event data (end time before start time)
        start_time = timezone.now() + timedelta(days=1)
        end_time = start_time - timedelta(hours=2)
        
        event_data = {
            'eventName': 'Invalid Test Booking',
            'startTime': start_time.isoformat(),
            'endTime': end_time.isoformat(),
            'bookingType': 'job',
            'backColor': '#6aa84f',
            'jobID': self.job.pk
        }
        
        response = self.client.post(self.create_event_url, event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify no new booking was created
        self.assertEqual(Booking.objects.count(), 1)
    
    def test_edit_event_unauthenticated(self):
        """Test that unauthenticated users cannot edit events"""
        response = self.client.post(self.edit_event_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_edit_event_authenticated(self):
        """Test that authenticated users can edit events"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare updated event data
        start_time = timezone.now() + timedelta(days=2)
        end_time = start_time + timedelta(hours=3)
        
        event_data = {
            'eventName': 'Updated Test Booking',
            'startTime': start_time.isoformat(),
            'endTime': end_time.isoformat(),
            'bookingType': 'quote',
            'backColor': '#ff0000',
            'status': 'accepted',
            'jobID': self.job.pk
        }
        
        response = self.client.post(self.edit_event_url, event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the booking was updated
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.event_name, 'Updated Test Booking')
        self.assertEqual(self.booking.booking_type, 'quote')
        self.assertEqual(self.booking.status, 'accepted')
        self.assertEqual(self.booking.back_color, '#ff0000')
    
    def test_delete_event_unauthenticated(self):
        """Test that unauthenticated users cannot delete events"""
        response = self.client.post(self.delete_event_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_event_authenticated(self):
        """Test that authenticated users can delete events"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(self.delete_event_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the booking was deleted
        self.assertEqual(Booking.objects.count(), 0)
    
    def test_delete_nonexistent_event(self):
        """Test deleting a nonexistent event"""
        self.client.force_authenticate(user=self.user)
        
        # Try to delete a nonexistent booking
        nonexistent_url = reverse('delete_event', args=[999])
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)