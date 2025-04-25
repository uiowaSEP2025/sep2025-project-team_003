from django.test import TestCase
from django.contrib.auth.models import User
from hsabackend.models.request import Request
from hsabackend.models.organization import Organization
from hsabackend.models.job import Job
from hsabackend.models.customer import Customer

class RequestModelTest(TestCase):
    def setUp(self):
        # Create a user for the organization
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create an organization
        self.organization = Organization.objects.create(
            org_name='Test Organization',
            org_email='org@example.com',
            org_city='Test City',
            org_state='CA',
            org_zip='12345',
            org_address='123 Test St',
            org_phone='1234567890',
            org_owner_first_name='Test',
            org_owner_last_name='Owner',
            owning_user=self.user
        )
        
        # Create a customer
        self.customer = Customer.objects.create(
            first_name='Test',
            last_name='Customer',
            email='customer@example.com',
            phone='1234567890',
            notes='Test notes',
            organization=self.organization
        )
        
        # Create a job
        self.job = Job.objects.create(
            job_status='created',
            description='Test Job Description',
            organization=self.organization,
            customer=self.customer,
            job_city='Test City',
            job_state='CA',
            job_zip='12345',
            job_address='123 Test St'
        )
        
        # Create a request
        self.request = Request.objects.create(
            requester_first_name='Test',
            requester_last_name='Requester',
            requester_email='requester@example.com',
            requester_city='Test City',
            requester_state='CA',
            requester_zip='12345',
            requester_address='123 Test St',
            requester_phone='1234567890',
            description='Test Request Description',
            availability='Weekdays 9-5',
            request_status='received',
            organization=self.organization,
            job=self.job
        )
    
    def test_request_creation(self):
        """Test that a request can be created with the expected values"""
        self.assertEqual(self.request.requester_first_name, 'Test')
        self.assertEqual(self.request.requester_last_name, 'Requester')
        self.assertEqual(self.request.requester_email, 'requester@example.com')
        self.assertEqual(self.request.requester_city, 'Test City')
        self.assertEqual(self.request.requester_state, 'CA')
        self.assertEqual(self.request.requester_zip, '12345')
        self.assertEqual(self.request.requester_address, '123 Test St')
        self.assertEqual(self.request.requester_phone, '1234567890')
        self.assertEqual(self.request.description, 'Test Request Description')
        self.assertEqual(self.request.availability, 'Weekdays 9-5')
        self.assertEqual(self.request.request_status, 'received')
        self.assertEqual(self.request.organization, self.organization)
        self.assertEqual(self.request.job, self.job)
    
    def test_str_method(self):
        """Test the __str__ method returns the expected string representation"""
        expected_str = f"<Request, name: {self.request.requester_first_name} {self.request.requester_last_name}, address: {self.request.requester_address}>"
        self.assertEqual(str(self.request), expected_str)
    
    def test_json_method(self):
        """Test the json method returns the expected dictionary"""
        expected_json = {
            'id': self.request.id,
            'requester_first_name': self.request.requester_first_name,
            'requester_last_name': self.request.requester_last_name,
            'requester_email': self.request.requester_email,
            'requester_city': self.request.requester_city,
            'requester_state': self.request.requester_state,
            'requester_zip': self.request.requester_zip,
            'requester_address': self.request.requester_address,
            'description': self.request.description,
            'status': self.request.request_status
        }
        self.assertEqual(self.request.json(), expected_json)
    
    def test_validators(self):
        """Test that validators are applied to the fields"""
        # Create a request with invalid values
        with self.assertRaises(Exception):
            Request.objects.create(
                requester_first_name='',  # Empty name should fail
                requester_last_name='Requester',
                requester_email='requester@example.com',
                requester_city='Test City',
                requester_state='CA',
                requester_zip='12345',
                requester_address='123 Test St',
                requester_phone='1234567890',
                description='Test Request Description',
                availability='Weekdays 9-5',
                organization=self.organization,
                job=self.job
            )
        
        with self.assertRaises(Exception):
            Request.objects.create(
                requester_first_name='Test',
                requester_last_name='Requester',
                requester_email='requester@example.com',
                requester_city='Test City',
                requester_state='XX',  # Invalid state should fail
                requester_zip='12345',
                requester_address='123 Test St',
                requester_phone='1234567890',
                description='Test Request Description',
                availability='Weekdays 9-5',
                organization=self.organization,
                job=self.job
            )
        
        with self.assertRaises(Exception):
            Request.objects.create(
                requester_first_name='Test',
                requester_last_name='Requester',
                requester_email='requester@example.com',
                requester_city='Test City',
                requester_state='CA',
                requester_zip='12345',
                requester_address='123 Test St',
                requester_phone='123456789',  # Invalid phone (too short) should fail
                description='Test Request Description',
                availability='Weekdays 9-5',
                organization=self.organization,
                job=self.job
            )
    
    def test_status_choices(self):
        """Test that request_status can only be set to valid choices"""
        # Test valid choices
        for status in ['received', 'approved']:
            self.request.request_status = status
            self.request.save()
            self.assertEqual(self.request.request_status, status)