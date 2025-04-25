from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from hsabackend.models.material import Material
from hsabackend.models.organization import Organization

class MaterialModelTest(TestCase):
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
        
        # Create a material
        self.material = Material.objects.create(
            material_name='Test Material',
            material_description='Test Material Description',
            organization=self.organization,
            default_cost=Decimal('50.00')
        )
    
    def test_material_creation(self):
        """Test that a material can be created with the expected values"""
        self.assertEqual(self.material.material_name, 'Test Material')
        self.assertEqual(self.material.material_description, 'Test Material Description')
        self.assertEqual(self.material.organization, self.organization)
        self.assertEqual(self.material.default_cost, Decimal('50.00'))
    
    def test_str_method(self):
        """Test the __str__ method returns the expected string representation"""
        expected_str = f"<Material, name: {self.material.material_name}, organization: {self.organization}>"
        self.assertEqual(str(self.material), expected_str)
    
    def test_json_method(self):
        """Test the json method returns the expected dictionary"""
        expected_json = {
            'id': self.material.pk,
            'material_name': self.material.material_name,
            'material_description': self.material.material_description,
            'default_cost': self.material.default_cost,
        }
        self.assertEqual(self.material.json(), expected_json)
    
    def test_validators(self):
        """Test that validators are applied to the fields"""
        # Create a material with invalid values
        with self.assertRaises(Exception):
            Material.objects.create(
                material_name='',  # Empty name should fail
                material_description='Test Material Description',
                organization=self.organization,
                default_cost=Decimal('50.00')
            )
    
    def test_optional_fields(self):
        """Test that optional fields can be null or blank"""
        # Create a material without a description
        material = Material.objects.create(
            material_name='Test Material 2',
            material_description=None,  # Null description should be allowed
            organization=self.organization,
            default_cost=Decimal('75.00')
        )
        
        self.assertIsNone(material.material_description)
        
        # Create a material with an empty description
        material = Material.objects.create(
            material_name='Test Material 3',
            material_description='',  # Empty description should be allowed
            organization=self.organization,
            default_cost=Decimal('100.00')
        )
        
        self.assertEqual(material.material_description, '')
        
        # Create a material without a default cost
        material = Material.objects.create(
            material_name='Test Material 4',
            material_description='Test Material Description 4',
            organization=self.organization,
            default_cost=Decimal('0.00')  # Default cost can be 0
        )
        
        self.assertEqual(material.default_cost, Decimal('0.00'))
    
    def test_multiple_materials(self):
        """Test that multiple materials can be created for the same organization"""
        # Create additional materials
        material2 = Material.objects.create(
            material_name='Test Material 2',
            material_description='Test Material Description 2',
            organization=self.organization,
            default_cost=Decimal('75.00')
        )
        
        material3 = Material.objects.create(
            material_name='Test Material 3',
            material_description='Test Material Description 3',
            organization=self.organization,
            default_cost=Decimal('100.00')
        )
        
        # Verify that all materials are associated with the same organization
        materials = Material.objects.filter(organization=self.organization)
        self.assertEqual(materials.count(), 3)
        self.assertIn(self.material, materials)
        self.assertIn(material2, materials)
        self.assertIn(material3, materials)