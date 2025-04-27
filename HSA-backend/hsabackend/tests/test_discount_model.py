from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from hsabackend.models.discount import Discount
from hsabackend.models.organization import Organization
from hsabackend.utils.string_formatters import format_percent

class DiscountModelTest(TestCase):
    """Test cases for the Discount model"""
    
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
        
        self.discount = Discount.objects.create(
            discount_name="Test Discount",
            discount_percent=Decimal('10.00'),
            organization=self.organization
        )
    
    def test_discount_creation(self):
        """Test that a discount can be created"""
        self.assertEqual(self.discount.discount_name, "Test Discount")
        self.assertEqual(self.discount.discount_percent, Decimal('10.00'))
        self.assertEqual(self.discount.organization, self.organization)
    
    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f"<Discount, organization: {self.organization}, percent: {self.discount.discount_percent}>"
        self.assertEqual(str(self.discount), expected_str)
    
    def test_json_for_discount_table_method(self):
        """Test the json_for_discount_table method"""
        expected_json = {
            "id": self.discount.pk, 
            "discount_name": "Test Discount",
            "discount_percent": format_percent(str(Decimal('10.00')))
        }
        self.assertEqual(self.discount.json_for_discount_table(), expected_json)
    
    def test_discount_name_validation(self):
        """Test discount_name field validation"""
        # Test empty discount_name
        discount = Discount(
            discount_name="",
            discount_percent=Decimal('10.00'),
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            discount.full_clean()
    
    def test_discount_percent_validation(self):
        """Test discount_percent field validation"""
        # Test negative discount_percent
        discount = Discount(
            discount_name="Test Discount",
            discount_percent=Decimal('-10.00'),
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            discount.full_clean()
        
        # Test discount_percent > 100
        discount = Discount(
            discount_name="Test Discount",
            discount_percent=Decimal('110.00'),
            organization=self.organization
        )
        with self.assertRaises(ValidationError):
            discount.full_clean()
        
        # Test valid discount_percent values
        valid_percents = [Decimal('0.00'), Decimal('50.00'), Decimal('100.00')]
        for percent in valid_percents:
            discount = Discount(
                discount_name="Test Discount",
                discount_percent=percent,
                organization=self.organization
            )
            discount.full_clean()  # Should not raise ValidationError