from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import json
from decimal import Decimal
from hsabackend.models.discount import Discount
from hsabackend.models.organization import Organization

class DiscountsViewsTest(TestCase):
    """Test cases for the Discounts views"""
    
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
        
        # Create a discount
        self.discount = Discount.objects.create(
            discount_name="Test Discount",
            discount_percent=Decimal('10.00'),
            organization=self.organization
        )
        
        # Set up the API client
        self.client = APIClient()
        
        # URLs
        self.get_discounts_url = reverse('get_discounts')
        self.create_discount_url = reverse('create_discount')
        self.edit_discount_url = reverse('edit_discount', args=[self.discount.pk])
        self.delete_discount_url = reverse('delete_discount', args=[self.discount.pk])
    
    def test_get_discounts_unauthenticated(self):
        """Test that unauthenticated users cannot get discounts"""
        response = self.client.get(self.get_discounts_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_discounts_authenticated(self):
        """Test that authenticated users can get discounts"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_discounts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertEqual(len(data['data']), 1)  # Should have one discount
    
    def test_create_discount_unauthenticated(self):
        """Test that unauthenticated users cannot create discounts"""
        response = self.client.post(self.create_discount_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_discount_authenticated(self):
        """Test that authenticated users can create discounts"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare discount data
        discount_data = {
            'discount_name': 'New Discount',
            'discount_percent': '15.00'
        }
        
        response = self.client.post(self.create_discount_url, discount_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the discount was created
        self.assertEqual(Discount.objects.count(), 2)
        new_discount = Discount.objects.get(discount_name='New Discount')
        self.assertEqual(new_discount.discount_percent, Decimal('15.00'))
    
    def test_create_discount_invalid_data(self):
        """Test that discounts cannot be created with invalid data"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare invalid discount data (missing required fields)
        discount_data = {
            'discount_name': '',
            'discount_percent': '-10.00'  # Negative percentage is invalid
        }
        
        response = self.client.post(self.create_discount_url, discount_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify no new discount was created
        self.assertEqual(Discount.objects.count(), 1)
    
    def test_edit_discount_unauthenticated(self):
        """Test that unauthenticated users cannot edit discounts"""
        response = self.client.post(self.edit_discount_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_edit_discount_authenticated(self):
        """Test that authenticated users can edit discounts"""
        self.client.force_authenticate(user=self.user)
        
        # Prepare updated discount data
        discount_data = {
            'discount_name': 'Updated Discount',
            'discount_percent': '20.00'
        }
        
        response = self.client.post(self.edit_discount_url, discount_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the discount was updated
        self.discount.refresh_from_db()
        self.assertEqual(self.discount.discount_name, 'Updated Discount')
        self.assertEqual(self.discount.discount_percent, Decimal('20.00'))
    
    def test_delete_discount_unauthenticated(self):
        """Test that unauthenticated users cannot delete discounts"""
        response = self.client.post(self.delete_discount_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_discount_authenticated(self):
        """Test that authenticated users can delete discounts"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(self.delete_discount_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the discount was deleted
        self.assertEqual(Discount.objects.count(), 0)
    
    def test_delete_nonexistent_discount(self):
        """Test deleting a nonexistent discount"""
        self.client.force_authenticate(user=self.user)
        
        # Try to delete a nonexistent discount
        nonexistent_url = reverse('delete_discount', args=[999])
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)