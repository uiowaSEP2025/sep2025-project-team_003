from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ValidationError
from hsabackend.models.contractor import Contractor
from hsabackend.models.organization import Organization
from hsabackend.utils.string_formatters import format_phone_number

class ContractorModelTest(TestCase):
    """Test cases for the Contractor model"""
    
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
            org_state="AZ",
            org_zip="12345",
            org_address="123 Test St",
            org_phone="1234567890",
            org_owner_first_name="John",
            org_owner_last_name="Doe",
            owning_user=self.user,
            is_onboarding=False,
            default_labor_rate=50.00
        )

        self.contractor = Contractor.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            organization=self.organization
        )
    
    def test_contractor_creation(self):
        """Test that a contractor can be created"""
        self.assertEqual(self.contractor.first_name, "John")
        self.assertEqual(self.contractor.last_name, "Doe")
        self.assertEqual(self.contractor.email, "john.doe@example.com")
        self.assertEqual(self.contractor.phone, "1234567890")
        self.assertEqual(self.contractor.organization, self.organization)
    
    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f"<Contractor: {self.contractor.pk}>"
        self.assertEqual(str(self.contractor), expected_str)
    
    def test_json_method(self):
        """Test the json method"""
        expected_json = {
            'id': self.contractor.pk,
            'first_name': "John",
            'last_name': "Doe",
            'email': "john.doe@example.com",
            'phone': format_phone_number("1234567890"),
        }
        self.assertEqual(self.contractor.json(), expected_json)
    
    def test_first_name_validation(self):
        """Test first_name field validation"""
        # Test empty first_name
        contractor = Contractor(
            first_name="",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            contractor.full_clean()
    
    def test_last_name_validation(self):
        """Test last_name field validation"""
        # Test empty last_name
        contractor = Contractor(
            first_name="John",
            last_name="",
            email="john.doe@example.com",
            phone="1234567890",
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            contractor.full_clean()
    
    def test_phone_validation(self):
        """Test phone field validation"""
        # Test invalid phone number
        contractor = Contractor(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="invalid",
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            contractor.full_clean()