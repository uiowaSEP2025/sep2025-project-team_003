from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from hsabackend.models.service import Service
from hsabackend.models.organization import Organization
from django.contrib.auth.models import User

class ServiceModelTest(TestCase):
    """Test cases for the Service model"""
    
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
            default_labor_rate=Decimal('50.00')
        )
        
        self.service = Service.objects.create(
            name="Test Service",
            description="Test Service Description",
            organization=self.organization,
            default_fee=Decimal('100.00')
        )
    
    def test_service_creation(self):
        """Test that a service can be created"""
        self.assertEqual(self.service.name, "Test Service")
        self.assertEqual(self.service.description, "Test Service Description")
        self.assertEqual(self.service.organization, self.organization)
        self.assertEqual(self.service.default_fee, Decimal('100.00'))
    
    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f"<Service, service_name: {self.service.name}, owning_org: {self.organization}>"
        self.assertEqual(str(self.service), expected_str)
    
    def test_json_method(self):
        """Test the json method"""
        expected_json = {
            'id': self.service.pk,
            'name': "Test Service",
            'description': "Test Service Description",
            'default_fee': Decimal('100.00'),
        }
        self.assertEqual(self.service.json(), expected_json)
    
    def test_name_validation(self):
        """Test name field validation"""
        # Test empty name
        service = Service(
            name="",
            description="Test Service Description",
            organization=self.organization,
            default_fee=Decimal('100.00')
        )
        with self.assertRaises(ValidationError):
            service.full_clean()
    
    def test_description_optional(self):
        """Test that description is optional"""
        # Create a service without a description
        service = Service.objects.create(
            name="No Description Service",
            description="",
            organization=self.organization,
            default_fee=Decimal('100.00')
        )
        self.assertEqual(service.description, "")
        service.full_clean()  # Should not raise ValidationError
    
    def test_default_fee_optional(self):
        """Test that default_fee is optional"""
        # Create a service without a default_fee
        service = Service.objects.create(
            name="No Default Fee Service",
            description="Test Service Description",
            organization=self.organization
        )
        self.assertEqual(service.default_fee, Decimal('0'))
        service.full_clean()  # Should not raise ValidationError