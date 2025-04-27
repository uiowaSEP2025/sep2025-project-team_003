from django.test import TestCase
from django.core.exceptions import ValidationError
from hsabackend.models.customer import Customer
from hsabackend.models.organization import Organization
from hsabackend.utils.string_formatters import format_phone_number

class CustomerModelTest(TestCase):
    """Test cases for the Customer model"""
    
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
        
        self.customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone="1234567890",
            notes="Test notes",
            organization=self.organization
        )
    
    def test_customer_creation(self):
        """Test that a customer can be created"""
        self.assertEqual(self.customer.first_name, "Jane")
        self.assertEqual(self.customer.last_name, "Smith")
        self.assertEqual(self.customer.email, "jane.smith@example.com")
        self.assertEqual(self.customer.phone, "1234567890")
        self.assertEqual(self.customer.notes, "Test notes")
        self.assertEqual(self.customer.organization, self.organization)
    
    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f"<Customer: {self.customer.pk}>"
        self.assertEqual(str(self.customer), expected_str)
    
    def test_json_method(self):
        """Test the json method"""
        expected_json = {
            'id': self.customer.pk,
            'first_name': "Jane",
            'last_name': "Smith",
            'email': "jane.smith@example.com",
            'phone': format_phone_number("1234567890"),
            'notes': "Test notes",
        }
        self.assertEqual(self.customer.json(), expected_json)
    
    def test_first_name_validation(self):
        """Test first_name field validation"""
        # Test empty first_name
        customer = Customer(
            first_name="",
            last_name="Smith",
            email="jane.smith@example.com",
            phone="1234567890",
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()
    
    def test_last_name_validation(self):
        """Test last_name field validation"""
        # Test empty last_name
        customer = Customer(
            first_name="Jane",
            last_name="",
            email="jane.smith@example.com",
            phone="1234567890",
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()
    
    def test_phone_validation(self):
        """Test phone field validation"""
        # Test invalid phone number
        customer = Customer(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone="invalid",
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()
    
    def test_notes_optional(self):
        """Test that notes field is optional"""
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            notes=None,
            organization=self.organization
        )
        self.assertIsNone(customer.notes)
        customer.full_clean()  # Should not raise ValidationError