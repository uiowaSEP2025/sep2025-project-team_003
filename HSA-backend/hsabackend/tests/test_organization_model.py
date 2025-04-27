from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from decimal import Decimal
from hsabackend.models.organization import Organization

class OrganizationModelTest(TestCase):
    """Test cases for the Organization model"""
    
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
            is_onboarding=True,
            default_labor_rate=Decimal('50.00'),
            default_payment_link="https://example.com/payment"
        )
    
    def test_organization_creation(self):
        """Test that an organization can be created"""
        self.assertEqual(self.organization.org_name, "Test Organization")
        self.assertEqual(self.organization.org_email, "test@example.com")
        self.assertEqual(self.organization.org_city, "Test City")
        self.assertEqual(self.organization.org_state, "TS")
        self.assertEqual(self.organization.org_zip, "12345")
        self.assertEqual(self.organization.org_address, "123 Test St")
        self.assertEqual(self.organization.org_phone, "1234567890")
        self.assertEqual(self.organization.org_owner_first_name, "John")
        self.assertEqual(self.organization.org_owner_last_name, "Doe")
        self.assertEqual(self.organization.owning_user, self.user)
        self.assertEqual(self.organization.is_onboarding, True)
        self.assertEqual(self.organization.default_labor_rate, Decimal('50.00'))
        self.assertEqual(self.organization.default_payment_link, "https://example.com/payment")
    
    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f"<Organization, org_name: {self.organization.org_name}>"
        self.assertEqual(str(self.organization), expected_str)
    
    def test_json_method(self):
        """Test the json method"""
        expected_json = {
            'org_name': "Test Organization",
            'org_email': "test@example.com",
            'org_phone': "1234567890",
            'org_city': "Test City",
            'org_state': "TS",
            'org_zip': "12345",
            'org_address': "123 Test St",
            'org_owner_first_name': "John",
            'org_owner_last_name': "Doe",
            'owning_user': self.user.id,
            'is_onboarding': True,
            'default_labor_rate': Decimal('50.00')
        }
        self.assertEqual(self.organization.json(), expected_json)
    
    def test_org_name_validation(self):
        """Test org_name field validation"""
        # Test empty org_name
        organization = Organization(
            org_name="",
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
        with self.assertRaises(ValidationError):
            organization.full_clean()
    
    def test_org_state_validation(self):
        """Test org_state field validation"""
        # Test invalid state
        organization = Organization(
            org_name="Test Organization",
            org_email="test@example.com",
            org_city="Test City",
            org_state="Invalid",
            org_zip="12345",
            org_address="123 Test St",
            org_phone="1234567890",
            org_owner_first_name="John",
            org_owner_last_name="Doe",
            owning_user=self.user,
            default_labor_rate=Decimal('50.00')
        )
        with self.assertRaises(ValidationError):
            organization.full_clean()
    
    def test_org_phone_validation(self):
        """Test org_phone field validation"""
        # Test invalid phone number
        organization = Organization(
            org_name="Test Organization",
            org_email="test@example.com",
            org_city="Test City",
            org_state="TS",
            org_zip="12345",
            org_address="123 Test St",
            org_phone="invalid",
            org_owner_first_name="John",
            org_owner_last_name="Doe",
            owning_user=self.user,
            default_labor_rate=Decimal('50.00')
        )
        with self.assertRaises(ValidationError):
            organization.full_clean()
    
    def test_default_payment_link_optional(self):
        """Test that default_payment_link is optional"""
        # Create an organization without a default_payment_link
        organization = Organization.objects.create(
            org_name="No Payment Link Organization",
            org_email="test@example.com",
            org_city="Test City",
            org_state="TS",
            org_zip="12345",
            org_address="123 Test St",
            org_phone="1234567890",
            org_owner_first_name="John",
            org_owner_last_name="Doe",
            owning_user=self.user,
            default_labor_rate=Decimal('50.00'),
            default_payment_link=""
        )
        self.assertEqual(organization.default_payment_link, "")
        organization.full_clean()  # Should not raise ValidationError