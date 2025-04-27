from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from hsabackend.models.material import Material
from hsabackend.models.organization import Organization

class MaterialModelTest(TestCase):
    """Test cases for the Material model"""
    
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
        
        self.material = Material.objects.create(
            name="Test Material",
            description="Test Material Description",
            organization=self.organization,
            default_cost=Decimal('10.00')
        )
    
    def test_material_creation(self):
        """Test that a material can be created"""
        self.assertEqual(self.material.name, "Test Material")
        self.assertEqual(self.material.description, "Test Material Description")
        self.assertEqual(self.material.organization, self.organization)
        self.assertEqual(self.material.default_cost, Decimal('10.00'))
    
    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f"<Material, name: {self.material.name}, organization: {self.organization}>"
        self.assertEqual(str(self.material), expected_str)
    
    def test_json_method(self):
        """Test the json method"""
        expected_json = {
            'id': self.material.pk,
            'name': "Test Material",
            'description': "Test Material Description",
            'default_cost': Decimal('10.00'),
        }
        self.assertEqual(self.material.json(), expected_json)
    
    def test_name_validation(self):
        """Test name field validation"""
        # Test empty name
        material = Material(
            name="",
            description="Test Material Description",
            organization=self.organization,
            default_cost=Decimal('10.00')
        )
        with self.assertRaises(ValidationError):
            material.full_clean()
    
    def test_description_optional(self):
        """Test that description is optional"""
        # Create a material without a description
        material = Material.objects.create(
            name="No Description Material",
            description=None,
            organization=self.organization,
            default_cost=Decimal('10.00')
        )
        self.assertIsNone(material.description)
        material.full_clean()  # Should not raise ValidationError
    
    def test_default_cost_optional(self):
        """Test that default_cost is optional"""
        # Create a material without a default_cost
        material = Material.objects.create(
            name="No Default Cost Material",
            description="Test Material Description",
            organization=self.organization
        )
        self.assertEqual(material.default_cost, Decimal('0'))
        material.full_clean()  # Should not raise ValidationError