from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
import json

from hsabackend.models.organization import Organization
from hsabackend.models.service import Service

class ServicesViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create an organization for the user
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
            is_onboarding=False  # Set to False to pass the onboarding check
        )
        
        # Create some test services
        self.service1 = Service.objects.create(
            service_name='Test Service 1',
            service_description='Test Service Description 1',
            organization=self.organization,
            default_fee=Decimal('100.00')
        )
        
        self.service2 = Service.objects.create(
            service_name='Test Service 2',
            service_description='Test Service Description 2',
            organization=self.organization,
            default_fee=Decimal('150.00')
        )
        
        # Set up the API client
        self.client = APIClient()
        
    def test_get_service_table_data_unauthenticated(self):
        """Test that unauthenticated users cannot access the get_service_table_data endpoint"""
        url = reverse('get_service_table_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_service_table_data_authenticated(self):
        """Test that authenticated users can access the get_service_table_data endpoint"""
        url = reverse('get_service_table_data')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the response contains the expected data
        data = json.loads(response.content)
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 2)  # We created 2 services
        
        # Check that the services have the expected properties
        service_names = [service['service_name'] for service in data['results']]
        self.assertIn('Test Service 1', service_names)
        self.assertIn('Test Service 2', service_names)
    
    def test_get_service_excluded_table_data(self):
        """Test the get_service_excluded_table_data endpoint"""
        url = reverse('get_service_excluded_table_data')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_service(self):
        """Test creating a new service"""
        url = reverse('create_service')
        self.client.force_authenticate(user=self.user)
        
        # Data for the new service
        new_service_data = {
            'service_name': 'New Test Service',
            'service_description': 'New Test Service Description',
            'default_fee': '200.00'
        }
        
        response = self.client.post(url, new_service_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that the service was created in the database
        self.assertTrue(Service.objects.filter(service_name='New Test Service').exists())
        
        # Check that the service has the expected properties
        service = Service.objects.get(service_name='New Test Service')
        self.assertEqual(service.service_description, 'New Test Service Description')
        self.assertEqual(service.default_fee, Decimal('200.00'))
        self.assertEqual(service.organization, self.organization)
    
    def test_edit_service(self):
        """Test editing an existing service"""
        url = reverse('edit_service', args=[self.service1.id])
        self.client.force_authenticate(user=self.user)
        
        # Data for updating the service
        updated_service_data = {
            'service_name': 'Updated Test Service',
            'service_description': 'Updated Test Service Description',
            'default_fee': '250.00'
        }
        
        response = self.client.post(url, updated_service_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the service was updated in the database
        self.service1.refresh_from_db()
        self.assertEqual(self.service1.service_name, 'Updated Test Service')
        self.assertEqual(self.service1.service_description, 'Updated Test Service Description')
        self.assertEqual(self.service1.default_fee, Decimal('250.00'))
    
    def test_delete_service(self):
        """Test deleting a service"""
        url = reverse('delete_service', args=[self.service1.id])
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the service was deleted from the database
        self.assertFalse(Service.objects.filter(id=self.service1.id).exists())
    
    def test_onboarding_check(self):
        """Test that views with require_onboarding=True reject users in onboarding"""
        # Set the organization to onboarding
        self.organization.is_onboarding = True
        self.organization.save()
        
        # Try to access get_service_table_data, which requires onboarding to be complete
        url = reverse('get_service_table_data')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to access create_service, which does not require onboarding to be complete
        url = reverse('create_service')
        response = self.client.post(url, {'service_name': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)