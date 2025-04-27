from django.test import TestCase
from django.core.exceptions import ValidationError
from hsabackend.models.request import Request
from hsabackend.models.organization import Organization
from hsabackend.models.job import Job
from django.contrib.auth.models import User

class RequestModelTest(TestCase):
    """Test cases for the Request model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        
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
            default_labor_rate=50.00
        )
        
        self.job = Job.objects.create(
            job_status="created",
            description="Test Job Description",
            organization=self.organization,
            job_city="Test City",
            job_state="TS",
            job_zip="12345",
            job_address="456 Test Ave"
        )
        
        self.request = Request.objects.create(
            requester_first_name="Jane",
            requester_last_name="Smith",
            requester_email="jane.smith@example.com",
            requester_city="Test City",
            requester_state="TS",
            requester_zip="12345",
            requester_address="789 Test Blvd",
            requester_phone="1234567890",
            description="Test Request Description",
            availability="Weekdays 9-5",
            request_status="received",
            organization=self.organization,
            job=self.job
        )
    
    def test_request_creation(self):
        """Test that a request can be created"""
        self.assertEqual(self.request.requester_first_name, "Jane")
        self.assertEqual(self.request.requester_last_name, "Smith")
        self.assertEqual(self.request.requester_email, "jane.smith@example.com")
        self.assertEqual(self.request.requester_city, "Test City")
        self.assertEqual(self.request.requester_state, "TS")
        self.assertEqual(self.request.requester_zip, "12345")
        self.assertEqual(self.request.requester_address, "789 Test Blvd")
        self.assertEqual(self.request.requester_phone, "1234567890")
        self.assertEqual(self.request.description, "Test Request Description")
        self.assertEqual(self.request.availability, "Weekdays 9-5")
        self.assertEqual(self.request.request_status, "received")
        self.assertEqual(self.request.organization, self.organization)
        self.assertEqual(self.request.job, self.job)
    
    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f"<Request, name: {self.request.requester_first_name} {self.request.requester_last_name}, address: {self.request.requester_address}>"
        self.assertEqual(str(self.request), expected_str)
    
    def test_json_method(self):
        """Test the json method"""
        expected_json = {
            'id': self.request.id,
            'requester_first_name': "Jane",
            'requester_last_name': "Smith",
            'requester_email': "jane.smith@example.com",
            'requester_city': "Test City",
            'requester_state': "TS",
            'requester_zip': "12345",
            'requester_address': "789 Test Blvd",
            'description': "Test Request Description",
            'status': "received"
        }
        self.assertEqual(self.request.json(), expected_json)
    
    def test_requester_first_name_validation(self):
        """Test requester_first_name field validation"""
        # Test empty requester_first_name
        request = Request(
            requester_first_name="",
            requester_last_name="Smith",
            requester_email="jane.smith@example.com",
            requester_city="Test City",
            requester_state="TS",
            requester_zip="12345",
            requester_address="789 Test Blvd",
            requester_phone="1234567890",
            description="Test Request Description",
            availability="Weekdays 9-5",
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            request.full_clean()
    
    def test_requester_state_validation(self):
        """Test requester_state field validation"""
        # Test invalid state
        request = Request(
            requester_first_name="Jane",
            requester_last_name="Smith",
            requester_email="jane.smith@example.com",
            requester_city="Test City",
            requester_state="Invalid",
            requester_zip="12345",
            requester_address="789 Test Blvd",
            requester_phone="1234567890",
            description="Test Request Description",
            availability="Weekdays 9-5",
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            request.full_clean()
    
    def test_requester_phone_validation(self):
        """Test requester_phone field validation"""
        # Test invalid phone number
        request = Request(
            requester_first_name="Jane",
            requester_last_name="Smith",
            requester_email="jane.smith@example.com",
            requester_city="Test City",
            requester_state="TS",
            requester_zip="12345",
            requester_address="789 Test Blvd",
            requester_phone="invalid",
            description="Test Request Description",
            availability="Weekdays 9-5",
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            request.full_clean()
    
    def test_job_optional(self):
        """Test that job is optional"""
        # Create a request without a job
        request = Request.objects.create(
            requester_first_name="John",
            requester_last_name="Doe",
            requester_email="john.doe@example.com",
            requester_city="Test City",
            requester_state="TS",
            requester_zip="12345",
            requester_address="101 Test Ave",
            requester_phone="1234567890",
            description="Another Test Request",
            availability="Weekends",
            organization=self.organization,
            job=None
        )
        self.assertIsNone(request.job)
        request.full_clean()  # Should not raise ValidationError
    
    def test_request_status_choices(self):
        """Test that request_status choices are enforced"""
        # Test all valid statuses
        for status in ["received", "approved"]:
            self.request.request_status = status
            self.request.save()
            self.assertEqual(self.request.request_status, status)