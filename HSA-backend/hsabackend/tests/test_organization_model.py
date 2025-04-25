from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from hsabackend.models.organization import Organization

class OrganizationModelTest(TestCase):
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
            owning_user=self.user,
            is_onboarding=True,
            default_labor_rate=Decimal('50.00'),
            default_payment_link='https://example.com/payment'
        )
    
    def test_organization_creation(self):
        """Test that an organization can be created with the expected values"""
        self.assertEqual(self.organization.org_name, 'Test Organization')
        self.assertEqual(self.organization.org_email, 'org@example.com')
        self.assertEqual(self.organization.org_city, 'Test City')
        self.assertEqual(self.organization.org_state, 'CA')
        self.assertEqual(self.organization.org_zip, '12345')
        self.assertEqual(self.organization.org_address, '123 Test St')
        self.assertEqual(self.organization.org_phone, '1234567890')
        self.assertEqual(self.organization.org_owner_first_name, 'Test')
        self.assertEqual(self.organization.org_owner_last_name, 'Owner')
        self.assertEqual(self.organization.owning_user, self.user)
        self.assertEqual(self.organization.is_onboarding, True)
        self.assertEqual(self.organization.default_labor_rate, Decimal('50.00'))
        self.assertEqual(self.organization.default_payment_link, 'https://example.com/payment')
    
    def test_str_method(self):
        """Test the __str__ method returns the expected string representation"""
        expected_str = f"<Organization, org_name: {self.organization.org_name}>"
        self.assertEqual(str(self.organization), expected_str)
    
    def test_json_method(self):
        """Test the json method returns the expected dictionary"""
        expected_json = {
            'org_name': self.organization.org_name,
            'org_email': self.organization.org_email,
            'org_phone': self.organization.org_phone,
            'org_city': self.organization.org_city,
            'org_state': self.organization.org_state,
            'org_zip': self.organization.org_zip,
            'org_address': self.organization.org_address,
            'org_owner_first_name': self.organization.org_owner_first_name,
            'org_owner_last_name': self.organization.org_owner_last_name,
            'owning_user': self.user.id,
            'is_onboarding': self.organization.is_onboarding,
            'default_labor_rate': self.organization.default_labor_rate
        }
        self.assertEqual(self.organization.json(), expected_json)
    
    def test_validators(self):
        """Test that validators are applied to the fields"""
        # Create an organization with invalid values
        with self.assertRaises(Exception):
            Organization.objects.create(
                org_name='',  # Empty name should fail
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
        
        with self.assertRaises(Exception):
            Organization.objects.create(
                org_name='Test Organization',
                org_email='org@example.com',
                org_city='Test City',
                org_state='XX',  # Invalid state should fail
                org_zip='12345',
                org_address='123 Test St',
                org_phone='1234567890',
                org_owner_first_name='Test',
                org_owner_last_name='Owner',
                owning_user=self.user
            )
        
        with self.assertRaises(Exception):
            Organization.objects.create(
                org_name='Test Organization',
                org_email='org@example.com',
                org_city='Test City',
                org_state='CA',
                org_zip='12345',
                org_address='123 Test St',
                org_phone='123456789',  # Invalid phone (too short) should fail
                org_owner_first_name='Test',
                org_owner_last_name='Owner',
                owning_user=self.user
            )
    
    def test_default_values(self):
        """Test that default values are set correctly"""
        # Create an organization without specifying default values
        org = Organization.objects.create(
            org_name='Test Organization 2',
            org_email='org2@example.com',
            org_city='Test City 2',
            org_state='CA',
            org_zip='54321',
            org_address='321 Test St',
            org_phone='0987654321',
            org_owner_first_name='Test 2',
            org_owner_last_name='Owner 2',
            owning_user=self.user
        )
        
        # Check that default values are set
        self.assertEqual(org.is_onboarding, True)
        self.assertEqual(org.default_labor_rate, Decimal('0'))
        self.assertEqual(org.default_payment_link, '')