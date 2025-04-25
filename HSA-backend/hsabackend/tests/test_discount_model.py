from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from hsabackend.models.discount import Discount
from hsabackend.models.organization import Organization
from hsabackend.utils.string_formatters import format_percent

class DiscountModelTest(TestCase):
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
        
        # Create a discount
        self.discount = Discount.objects.create(
            discount_name='Test Discount',
            discount_percent=Decimal('10.00'),
            organization=self.organization
        )
    
    def test_discount_creation(self):
        """Test that a discount can be created with the expected values"""
        self.assertEqual(self.discount.discount_name, 'Test Discount')
        self.assertEqual(self.discount.discount_percent, Decimal('10.00'))
        self.assertEqual(self.discount.organization, self.organization)
    
    def test_str_method(self):
        """Test the __str__ method returns the expected string representation"""
        expected_str = f"<Discount, organization: {self.organization}, percent: {self.discount.discount_percent}>"
        self.assertEqual(str(self.discount), expected_str)
    
    def test_json_for_discount_table_method(self):
        """Test the json_for_discount_table method returns the expected dictionary"""
        expected_json = {
            "id": self.discount.pk, 
            "discount_name": self.discount.discount_name,
            "discount_percent": format_percent(str(self.discount.discount_percent))
        }
        self.assertEqual(self.discount.json_for_discount_table(), expected_json)
    
    def test_validators(self):
        """Test that validators are applied to the fields"""
        # Create a discount with invalid values
        with self.assertRaises(Exception):
            Discount.objects.create(
                discount_name='',  # Empty name should fail
                discount_percent=Decimal('10.00'),
                organization=self.organization
            )
        
        with self.assertRaises(Exception):
            Discount.objects.create(
                discount_name='Test Discount',
                discount_percent=Decimal('101.00'),  # Percent > 100 should fail
                organization=self.organization
            )
        
        with self.assertRaises(Exception):
            Discount.objects.create(
                discount_name='Test Discount',
                discount_percent=Decimal('-1.00'),  # Negative percent should fail
                organization=self.organization
            )
    
    def test_discount_percent_range(self):
        """Test that discount_percent can be set to valid values within the range"""
        # Test valid values
        valid_percents = [Decimal('0.00'), Decimal('50.00'), Decimal('100.00')]
        for percent in valid_percents:
            discount = Discount.objects.create(
                discount_name=f'Test Discount {percent}',
                discount_percent=percent,
                organization=self.organization
            )
            self.assertEqual(discount.discount_percent, percent)