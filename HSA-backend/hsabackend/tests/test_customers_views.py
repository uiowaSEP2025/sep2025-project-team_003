from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import json
from hsabackend.models.customer import Customer
from hsabackend.models.organization import Organization

class CustomersViewsTest(TestCase):
    """Test cases for the Customers views"""
    
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
        
        # Create a customer
        self.customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone="1234567890",
            notes="Test notes",
            organization=self.organization
        )
        
        # Set up the API client
        self.client = APIClient()
        
        # URLs
        self.get_customer_table_data_url = reverse('get_customer_table_data')
        self.get_customer_excluded_table_data_url = reverse('get_customer_excluded_table_data')
        self.create_customer_url = reverse('create_customer')
        self.edit_customer_url = reverse('edit_customer', args=[self.customer.pk])
        self.delete_customer_url = reverse('delete_customer', args=[self.customer.pk])
    
    def test_get_customer_table_data_unauthenticated(self):
        """Test that unauthenticated users cannot get customer table data"""
        response = self.client.get(self.get_customer_table_data_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_customer_table_data_authenticated(self):
        """Test that authenticated users can get customer table data"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_customer_table_data_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertEqual(len(data['data']), 1)  # Should have one customer
    
    def test_get_customer_excluded_table_data_unauthenticated(self):
        """Test that unauthenticated users cannot get excluded customer table data"""
        response = self.client.get(self.get_customer_excluded_table_data_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_customer_excluded_table_data_authenticated(self):
        """Test that authenticated users can get excluded customer table data"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_customer_excluded_table_data_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_customer_unauthenticated(self):
        """Test that unauthenticated users cannot create customers"""
        response = self.client.post(self.create_customer_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_customer_authenticated(self):
        """Test that authenticated users can create customers"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare customer data
        customer_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '9876543210',
            'notes': 'New customer notes'
        }
        
        response = self.client.post(self.create_customer_url, customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the customer was created
        self.assertEqual(Customer.objects.count(), 2)
        new_customer = Customer.objects.get(email='john.doe@example.com')
        self.assertEqual(new_customer.first_name, 'John')
        self.assertEqual(new_customer.last_name, 'Doe')
        self.assertEqual(new_customer.notes, 'New customer notes')
    
    def test_create_customer_invalid_data(self):
        """Test that customers cannot be created with invalid data"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare invalid customer data (missing required fields)
        customer_data = {
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email',
            'phone': 'invalid-phone'
        }
        
        response = self.client.post(self.create_customer_url, customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify no new customer was created
        self.assertEqual(Customer.objects.count(), 1)
    
    def test_edit_customer_unauthenticated(self):
        """Test that unauthenticated users cannot edit customers"""
        response = self.client.post(self.edit_customer_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_edit_customer_authenticated(self):
        """Test that authenticated users can edit customers"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare updated customer data
        customer_data = {
            'first_name': 'Updated Jane',
            'last_name': 'Updated Smith',
            'email': 'updated.jane.smith@example.com',
            'phone': '5555555555',
            'notes': 'Updated notes'
        }
        
        response = self.client.post(self.edit_customer_url, customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the customer was updated
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'Updated Jane')
        self.assertEqual(self.customer.last_name, 'Updated Smith')
        self.assertEqual(self.customer.email, 'updated.jane.smith@example.com')
        self.assertEqual(self.customer.phone, '5555555555')
        self.assertEqual(self.customer.notes, 'Updated notes')
    
    def test_delete_customer_unauthenticated(self):
        """Test that unauthenticated users cannot delete customers"""
        response = self.client.post(self.delete_customer_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_customer_authenticated(self):
        """Test that authenticated users can delete customers"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(self.delete_customer_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the customer was deleted
        self.assertEqual(Customer.objects.count(), 0)
    
    def test_delete_nonexistent_customer(self):
        """Test deleting a nonexistent customer"""
        self.client.force_authenticate(user=self.user)
        
        # Try to delete a nonexistent customer
        nonexistent_url = reverse('delete_customer', args=[999])
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)