from django.test import TestCase
from django.contrib.auth.models import User
from hsabackend.models.contractor import Contractor
from hsabackend.models.organization import Organization
from hsabackend.utils.string_formatters import format_phone_number

class ContractorModelTest(TestCase):
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
        
        # Create a contractor
        self.contractor = Contractor.objects.create(
            first_name='Test',
            last_name='Contractor',
            email='contractor@example.com',
            phone='1234567890',
            organization=self.organization
        )
    
    def test_contractor_creation(self):
        """Test that a contractor can be created with the expected values"""
        self.assertEqual(self.contractor.first_name, 'Test')
        self.assertEqual(self.contractor.last_name, 'Contractor')
        self.assertEqual(self.contractor.email, 'contractor@example.com')
        self.assertEqual(self.contractor.phone, '1234567890')
        self.assertEqual(self.contractor.organization, self.organization)
    
    def test_str_method(self):
        """Test the __str__ method returns the expected string representation"""
        expected_str = f"<Contractor: {self.contractor.pk}>"
        self.assertEqual(str(self.contractor), expected_str)
    
    def test_json_method(self):
        """Test the json method returns the expected dictionary"""
        expected_json = {
            'id': self.contractor.pk,
            'first_name': self.contractor.first_name,
            'last_name': self.contractor.last_name,
            'email': self.contractor.email,
            'phone': format_phone_number(self.contractor.phone),
        }
        self.assertEqual(self.contractor.json(), expected_json)
    
    def test_validators(self):
        """Test that validators are applied to the fields"""
        # Create a contractor with invalid values
        with self.assertRaises(Exception):
            Contractor.objects.create(
                first_name='',  # Empty name should fail
                last_name='Contractor',
                email='contractor@example.com',
                phone='1234567890',
                organization=self.organization
            )
        
        with self.assertRaises(Exception):
            Contractor.objects.create(
                first_name='Test',
                last_name='',  # Empty last name should fail
                email='contractor@example.com',
                phone='1234567890',
                organization=self.organization
            )
        
        with self.assertRaises(Exception):
            Contractor.objects.create(
                first_name='Test',
                last_name='Contractor',
                email='contractor@example.com',
                phone='123456789',  # Invalid phone (too short) should fail
                organization=self.organization
            )
    
    def test_multiple_contractors(self):
        """Test that multiple contractors can be created for the same organization"""
        # Create additional contractors
        contractor2 = Contractor.objects.create(
            first_name='Test2',
            last_name='Contractor2',
            email='contractor2@example.com',
            phone='9876543210',
            organization=self.organization
        )
        
        contractor3 = Contractor.objects.create(
            first_name='Test3',
            last_name='Contractor3',
            email='contractor3@example.com',
            phone='5678901234',
            organization=self.organization
        )
        
        # Verify that all contractors are associated with the same organization
        contractors = Contractor.objects.filter(organization=self.organization)
        self.assertEqual(contractors.count(), 3)
        self.assertIn(self.contractor, contractors)
        self.assertIn(contractor2, contractors)
        self.assertIn(contractor3, contractors)