from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
import json
from datetime import date

from hsabackend.models.organization import Organization
from hsabackend.models.customer import Customer
from hsabackend.models.invoice import Invoice
from hsabackend.models.job import Job
from hsabackend.models.discount import Discount

class InvoicesViewsTest(TestCase):
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
        
        # Create a customer
        self.customer = Customer.objects.create(
            first_name='Test',
            last_name='Customer',
            email='customer@example.com',
            phone='1234567890',
            notes='Test notes',
            organization=self.organization
        )
        
        # Create discounts
        self.discount1 = Discount.objects.create(
            discount_name='Test Discount 1',
            discount_percent=Decimal('10.00'),
            organization=self.organization
        )
        
        self.discount2 = Discount.objects.create(
            discount_name='Test Discount 2',
            discount_percent=Decimal('5.00'),
            organization=self.organization
        )
        
        # Create an invoice
        self.invoice = Invoice.objects.create(
            date_issued=date(2023, 1, 1),
            date_due=date(2023, 1, 15),
            status='created',
            sales_tax_percent=Decimal('7.50'),
            customer=self.customer,
            payment_link='https://example.com/payment'
        )
        
        # Add discounts to the invoice
        self.invoice.discounts.add(self.discount1, self.discount2)
        
        # Create jobs linked to the invoice
        self.job1 = Job.objects.create(
            job_status='completed',
            description='Test Job 1',
            organization=self.organization,
            invoice=self.invoice,
            customer=self.customer,
            job_city='Test City',
            job_state='CA',
            job_zip='12345',
            job_address='123 Test St'
        )
        
        self.job2 = Job.objects.create(
            job_status='completed',
            description='Test Job 2',
            organization=self.organization,
            invoice=self.invoice,
            customer=self.customer,
            job_city='Test City',
            job_state='CA',
            job_zip='12345',
            job_address='123 Test St'
        )
        
        # Set up the API client
        self.client = APIClient()
    
    def test_get_invoices_unauthenticated(self):
        """Test that unauthenticated users cannot access the get_invoices endpoint"""
        url = reverse('get_invoices')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_invoices_authenticated(self):
        """Test that authenticated users can access the get_invoices endpoint"""
        url = reverse('get_invoices')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the response contains the expected data
        data = json.loads(response.content)
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)  # We created 1 invoice
        
        # Check that the invoice has the expected properties
        invoice = data['results'][0]
        self.assertEqual(invoice['status'], 'created')
        self.assertEqual(invoice['customer_name'], f"{self.customer.first_name}, {self.customer.last_name}")
    
    def test_create_invoice(self):
        """Test creating a new invoice"""
        url = reverse('create_invoice')
        self.client.force_authenticate(user=self.user)
        
        # Data for the new invoice
        new_invoice_data = {
            'customer': self.customer.id,
            'date_issued': '2023-02-01',
            'date_due': '2023-02-15',
            'status': 'created',
            'sales_tax_percent': '8.50',
            'payment_link': 'https://example.com/payment2'
        }
        
        response = self.client.post(url, new_invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that the invoice was created in the database
        self.assertEqual(Invoice.objects.count(), 2)
        
        # Check that the invoice has the expected properties
        invoice = Invoice.objects.latest('id')
        self.assertEqual(invoice.status, 'created')
        self.assertEqual(invoice.sales_tax_percent, Decimal('8.50'))
        self.assertEqual(invoice.customer, self.customer)
        self.assertEqual(invoice.payment_link, 'https://example.com/payment2')
    
    def test_update_invoice(self):
        """Test updating an existing invoice"""
        url = reverse('update_invoice', args=[self.invoice.id])
        self.client.force_authenticate(user=self.user)
        
        # Data for updating the invoice
        updated_invoice_data = {
            'customer': self.customer.id,
            'date_issued': '2023-03-01',
            'date_due': '2023-03-15',
            'status': 'issued',
            'sales_tax_percent': '9.50',
            'payment_link': 'https://example.com/payment3'
        }
        
        response = self.client.post(url, updated_invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the invoice was updated in the database
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, 'issued')
        self.assertEqual(self.invoice.sales_tax_percent, Decimal('9.50'))
        self.assertEqual(self.invoice.payment_link, 'https://example.com/payment3')
    
    def test_delete_invoice(self):
        """Test deleting an invoice"""
        url = reverse('delete_invoice', args=[self.invoice.id])
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the invoice was deleted from the database
        self.assertFalse(Invoice.objects.filter(id=self.invoice.id).exists())
        
        # Check that the jobs are no longer associated with the invoice
        self.job1.refresh_from_db()
        self.job2.refresh_from_db()
        self.assertIsNone(self.job1.invoice)
        self.assertIsNone(self.job2.invoice)
    
    def test_get_invoice(self):
        """Test retrieving a specific invoice"""
        url = reverse('get_invoice', args=[self.invoice.id])
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the response contains the expected data
        data = json.loads(response.content)
        self.assertEqual(data['id'], self.invoice.id)
        self.assertEqual(data['status'], self.invoice.status)
    
    def test_get_data_for_invoice(self):
        """Test retrieving detailed data for a specific invoice"""
        url = reverse('get_data_for_invoice', args=[self.invoice.id])
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the response contains the expected data
        data = json.loads(response.content)
        self.assertEqual(data['id'], self.invoice.id)
        self.assertEqual(data['status'], self.invoice.status)
        
        # Check that the jobs data is included
        self.assertIn('jobs', data)
        self.assertIn('jobs', data['jobs'])
        self.assertEqual(len(data['jobs']['jobs']), 2)  # We created 2 jobs
        
        # Check that the calculated totals are included
        self.assertIn('subtotal', data['jobs'])
        self.assertIn('taxPercent', data['jobs'])
        self.assertIn('totalDiscount', data['jobs'])
        self.assertIn('discountedSubtotal', data['jobs'])
        self.assertIn('subtotalAfterDiscount', data['jobs'])
        self.assertIn('taxableAmount', data['jobs'])
        self.assertIn('grandtotal', data['jobs'])
    
    def test_get_invoice_not_found(self):
        """Test retrieving a non-existent invoice"""
        url = reverse('get_invoice', args=[999])  # Non-existent ID
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_data_for_invoice_not_found(self):
        """Test retrieving detailed data for a non-existent invoice"""
        url = reverse('get_data_for_invoice', args=[999])  # Non-existent ID
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_onboarding_check(self):
        """Test that views with require_onboarding=True reject users in onboarding"""
        # Set the organization to onboarding
        self.organization.is_onboarding = True
        self.organization.save()
        
        # Try to access get_invoices, which requires onboarding to be complete
        url = reverse('get_invoices')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)