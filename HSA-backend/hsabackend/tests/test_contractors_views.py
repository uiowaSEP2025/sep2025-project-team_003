from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import json
from hsabackend.models.contractor import Contractor
from hsabackend.models.organization import Organization

class ContractorsViewsTest(TestCase):
    """Test cases for the Contractors views"""
    
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
            org_state="TS",
            org_zip="12345",
            org_address="123 Test St",
            org_phone="1234567890",
            org_owner_first_name="John",
            org_owner_last_name="Doe",
            owning_user=self.user,
            is_onboarding=False,
            default_labor_rate=50.00
        )
        
        # Create a contractor
        self.contractor = Contractor.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone="1234567890",
            organization=self.organization
        )
        
        # Set up the API client
        self.client = APIClient()
        
        # URLs
        self.get_contractor_table_data_url = reverse('get_contractor_table_data')
        self.get_contractor_excluded_table_data_url = reverse('get_contractor_excluded_table_data')
        self.create_contractor_url = reverse('create_contractor')
        self.edit_contractor_url = reverse('edit_contractor', args=[self.contractor.pk])
        self.delete_contractor_url = reverse('delete_contractor', args=[self.contractor.pk])
    
    def test_get_contractor_table_data_unauthenticated(self):
        """Test that unauthenticated users cannot get contractor table data"""
        response = self.client.get(self.get_contractor_table_data_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_contractor_table_data_authenticated(self):
        """Test that authenticated users can get contractor table data"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_contractor_table_data_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertEqual(len(data['data']), 1)  # Should have one contractor
    
    def test_get_contractor_excluded_table_data_unauthenticated(self):
        """Test that unauthenticated users cannot get excluded contractor table data"""
        response = self.client.get(self.get_contractor_excluded_table_data_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_contractor_excluded_table_data_authenticated(self):
        """Test that authenticated users can get excluded contractor table data"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_contractor_excluded_table_data_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_contractor_unauthenticated(self):
        """Test that unauthenticated users cannot create contractors"""
        response = self.client.post(self.create_contractor_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_contractor_authenticated(self):
        """Test that authenticated users can create contractors"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare contractor data
        contractor_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '9876543210'
        }
        
        response = self.client.post(self.create_contractor_url, contractor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the contractor was created
        self.assertEqual(Contractor.objects.count(), 2)
        new_contractor = Contractor.objects.get(email='john.doe@example.com')
        self.assertEqual(new_contractor.first_name, 'John')
        self.assertEqual(new_contractor.last_name, 'Doe')
    
    def test_create_contractor_invalid_data(self):
        """Test that contractors cannot be created with invalid data"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare invalid contractor data (missing required fields)
        contractor_data = {
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email',
            'phone': 'invalid-phone'
        }
        
        response = self.client.post(self.create_contractor_url, contractor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify no new contractor was created
        self.assertEqual(Contractor.objects.count(), 1)
    
    def test_edit_contractor_unauthenticated(self):
        """Test that unauthenticated users cannot edit contractors"""
        response = self.client.post(self.edit_contractor_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_edit_contractor_authenticated(self):
        """Test that authenticated users can edit contractors"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare updated contractor data
        contractor_data = {
            'first_name': 'Updated Jane',
            'last_name': 'Updated Smith',
            'email': 'updated.jane.smith@example.com',
            'phone': '5555555555'
        }
        
        response = self.client.post(self.edit_contractor_url, contractor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the contractor was updated
        self.contractor.refresh_from_db()
        self.assertEqual(self.contractor.first_name, 'Updated Jane')
        self.assertEqual(self.contractor.last_name, 'Updated Smith')
        self.assertEqual(self.contractor.email, 'updated.jane.smith@example.com')
        self.assertEqual(self.contractor.phone, '5555555555')
    
    def test_delete_contractor_unauthenticated(self):
        """Test that unauthenticated users cannot delete contractors"""
        response = self.client.post(self.delete_contractor_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_contractor_authenticated(self):
        """Test that authenticated users can delete contractors"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(self.delete_contractor_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the contractor was deleted
        self.assertEqual(Contractor.objects.count(), 0)
    
    def test_delete_nonexistent_contractor(self):
        """Test deleting a nonexistent contractor"""
        self.client.force_authenticate(user=self.user)
        
        # Try to delete a nonexistent contractor
        nonexistent_url = reverse('delete_contractor', args=[999])
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)