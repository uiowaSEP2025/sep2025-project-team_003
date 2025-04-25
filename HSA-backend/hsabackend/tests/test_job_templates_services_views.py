from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
import json

from hsabackend.models.organization import Organization
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.service import Service

# Define a JobTemplateService model for testing purposes
# This model mimics the expected behavior of the missing model
class JobTemplateService(models.Model):
    job_template = models.ForeignKey(JobTemplate, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    def json(self):
        return {
            'id': self.pk,
            'job_template': self.job_template.pk,
            'service': self.service.pk,
            'service_name': self.service.service_name,
            'service_description': self.service.service_description,
            'default_fee': str(self.service.default_fee)
        }

class JobTemplatesServicesViewsTest(TestCase):
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
        
        # Create a job template
        self.job_template = JobTemplate.objects.create(
            name='Test Job Template',
            description='Test Job Template Description',
            organization=self.organization
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
        
        # Create job template services
        self.job_template_service1 = JobTemplateService.objects.create(
            job_template=self.job_template,
            service=self.service1
        )
        
        # Set up the API client
        self.client = APIClient()
    
    def test_get_job_template_service_table_data_unauthenticated(self):
        """Test that unauthenticated users cannot access the get_job_template_service_table_data endpoint"""
        url = reverse('get_job_template_service_table_data', args=[self.job_template.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_job_template_service_table_data_authenticated(self):
        """Test that authenticated users can access the get_job_template_service_table_data endpoint"""
        url = reverse('get_job_template_service_table_data', args=[self.job_template.id])
        self.client.force_authenticate(user=self.user)
        
        # Add query parameters
        query_params = {'pagesize': '10', 'offset': '0'}
        response = self.client.get(url, query_params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the response contains the expected data
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertEqual(len(data['data']), 1)  # We created 1 job template service
        
        # Check that the job template service has the expected properties
        job_template_service = data['data'][0]
        self.assertEqual(job_template_service['service_name'], 'Test Service 1')
    
    def test_get_job_template_service_table_data_invalid_params(self):
        """Test that the get_job_template_service_table_data endpoint validates query parameters"""
        url = reverse('get_job_template_service_table_data', args=[self.job_template.id])
        self.client.force_authenticate(user=self.user)
        
        # Missing pagesize
        query_params = {'offset': '0'}
        response = self.client.get(url, query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Missing offset
        query_params = {'pagesize': '10'}
        response = self.client.get(url, query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Non-integer pagesize
        query_params = {'pagesize': 'abc', 'offset': '0'}
        response = self.client.get(url, query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Non-integer offset
        query_params = {'pagesize': '10', 'offset': 'abc'}
        response = self.client.get(url, query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_job_template_service(self):
        """Test creating a new job template service"""
        url = reverse('create_job_template_service', args=[self.job_template.id])
        self.client.force_authenticate(user=self.user)
        
        # Data for the new job template service
        new_job_template_service_data = {
            'services': [
                {
                    'id': self.service2.id
                }
            ]
        }
        
        response = self.client.post(url, new_job_template_service_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that the job template service was created in the database
        self.assertTrue(JobTemplateService.objects.filter(job_template=self.job_template, service=self.service2).exists())
    
    def test_create_job_template_service_empty_services(self):
        """Test creating a job template service with empty services list"""
        url = reverse('create_job_template_service', args=[self.job_template.id])
        self.client.force_authenticate(user=self.user)
        
        # Data with empty services list
        data = {
            'services': []
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_job_template_service_duplicate(self):
        """Test creating a duplicate job template service"""
        url = reverse('create_job_template_service', args=[self.job_template.id])
        self.client.force_authenticate(user=self.user)
        
        # Data for a duplicate job template service
        duplicate_data = {
            'services': [
                {
                    'id': self.service1.id
                }
            ]
        }
        
        response = self.client.post(url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_job_template_service(self):
        """Test deleting a job template service"""
        url = reverse('delete_job_template_service', args=[self.job_template.id, self.job_template_service1.id])
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the job template service was deleted from the database
        self.assertFalse(JobTemplateService.objects.filter(id=self.job_template_service1.id).exists())
    
    def test_delete_job_template_service_not_found(self):
        """Test deleting a non-existent job template service"""
        url = reverse('delete_job_template_service', args=[self.job_template.id, 999])  # Non-existent ID
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_cached_job_template_service(self):
        """Test deleting multiple job template services"""
        # Create another job template service
        job_template_service2 = JobTemplateService.objects.create(
            job_template=self.job_template,
            service=self.service2
        )
        
        url = reverse('delete_cached_job_template_service', args=[self.job_template.id])
        self.client.force_authenticate(user=self.user)
        
        # Data for deleting multiple job template services
        data = {
            'jobTemplateServices': [
                {
                    'id': self.job_template_service1.id
                },
                {
                    'id': job_template_service2.id
                }
            ]
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the job template services were deleted from the database
        self.assertFalse(JobTemplateService.objects.filter(id=self.job_template_service1.id).exists())
        self.assertFalse(JobTemplateService.objects.filter(id=job_template_service2.id).exists())
    
    def test_delete_cached_job_template_service_empty_list(self):
        """Test deleting with empty job template services list"""
        url = reverse('delete_cached_job_template_service', args=[self.job_template.id])
        self.client.force_authenticate(user=self.user)
        
        # Data with empty job template services list
        data = {
            'jobTemplateServices': []
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_cached_job_template_service_not_found(self):
        """Test deleting a non-existent job template service in the cached list"""
        url = reverse('delete_cached_job_template_service', args=[self.job_template.id])
        self.client.force_authenticate(user=self.user)
        
        # Data with non-existent job template service
        data = {
            'jobTemplateServices': [
                {
                    'id': 999  # Non-existent ID
                }
            ]
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)