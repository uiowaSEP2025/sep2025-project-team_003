from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from hsabackend.models.service import Service
from hsabackend.models.organization import Organization

class ServiceModelTest(TestCase):
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
        
        # Create a service
        self.service = Service.objects.create(
            service_name='Test Service',
            service_description='Test Service Description',
            organization=self.organization,
            default_fee=Decimal('100.00')
        )
    
    def test_service_creation(self):
        """Test that a service can be created with the expected values"""
        self.assertEqual(self.service.service_name, 'Test Service')
        self.assertEqual(self.service.service_description, 'Test Service Description')
        self.assertEqual(self.service.organization, self.organization)
        self.assertEqual(self.service.default_fee, Decimal('100.00'))
    
    def test_str_method(self):
        """Test the __str__ method returns the expected string representation"""
        expected_str = f"<Service, service_name: {self.service.service_name}, owning_org: {self.organization}>"
        self.assertEqual(str(self.service), expected_str)
    
    def test_json_method(self):
        """Test the json method returns the expected dictionary"""
        expected_json = {
            'id': self.service.pk,
            'service_name': self.service.service_name,
            'service_description': self.service.service_description,
            'default_fee': self.service.default_fee,
        }
        self.assertEqual(self.service.json(), expected_json)
    
    def test_validators(self):
        """Test that validators are applied to the fields"""
        # Create a service with invalid values
        with self.assertRaises(Exception):
            Service.objects.create(
                service_name='',  # Empty name should fail
                service_description='Test Service Description',
                organization=self.organization,
                default_fee=Decimal('100.00')
            )
    
    def test_optional_fields(self):
        """Test that optional fields can be blank"""
        # Create a service without a description
        service = Service.objects.create(
            service_name='Test Service 2',
            service_description='',  # Empty description should be allowed
            organization=self.organization,
            default_fee=Decimal('150.00')
        )
        
        self.assertEqual(service.service_description, '')
        
        # Create a service without a default fee
        service = Service.objects.create(
            service_name='Test Service 3',
            service_description='Test Service Description 3',
            organization=self.organization,
            default_fee=Decimal('0.00')  # Default fee can be 0
        )
        
        self.assertEqual(service.default_fee, Decimal('0.00'))
    
    def test_multiple_services(self):
        """Test that multiple services can be created for the same organization"""
        # Create additional services
        service2 = Service.objects.create(
            service_name='Test Service 2',
            service_description='Test Service Description 2',
            organization=self.organization,
            default_fee=Decimal('150.00')
        )
        
        service3 = Service.objects.create(
            service_name='Test Service 3',
            service_description='Test Service Description 3',
            organization=self.organization,
            default_fee=Decimal('200.00')
        )
        
        # Verify that all services are associated with the same organization
        services = Service.objects.filter(organization=self.organization)
        self.assertEqual(services.count(), 3)
        self.assertIn(self.service, services)
        self.assertIn(service2, services)
        self.assertIn(service3, services)