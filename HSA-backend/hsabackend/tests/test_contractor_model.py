from django.test import TestCase
from django.core.exceptions import ValidationError
from hsabackend.models.contractor import Contractor
from hsabackend.models.organization import Organization
from hsabackend.utils.string_formatters import format_phone_number

class ContractorModelTest(TestCase):
    """Test cases for the Contractor model"""
    
    def setUp(self):
        """Set up test data"""
        self.organization = Organization.objects.create(
            name="Test Organization",
            address="123 Test St",
            city="Test City",
            state="TS",
            zip_code="12345",
            phone="1234567890",
            email="test@example.com"
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