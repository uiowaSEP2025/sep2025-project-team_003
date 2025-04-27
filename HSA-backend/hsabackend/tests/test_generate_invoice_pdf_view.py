from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from decimal import Decimal
from datetime import date
from hsabackend.models.organization import Organization
from hsabackend.models.customer import Customer
from hsabackend.models.invoice import Invoice
from hsabackend.models.job import Job

class GenerateInvoicePDFViewTest(TestCase):
    """Test cases for the Generate Invoice PDF view"""
    
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
            default_labor_rate=Decimal('50.00')
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
        
        # Create an invoice
        self.invoice = Invoice.objects.create(
            date_issued=date(2023, 1, 1),
            date_due=date(2023, 1, 31),
            status="created",
            sales_tax_percent=Decimal('7.00'),
            customer=self.customer
        )
        
        # Create a job
        self.job = Job.objects.create(
            job_status="created",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 31),
            description="Test Job Description",
            organization=self.organization,
            invoice=self.invoice,
            customer=self.customer,
            job_city="Test City",
            job_state="TS",
            job_zip="12345",
            job_address="456 Test Ave"
        )
        
        # Set up the API client
        self.client = APIClient()
        
        # URL
        self.generate_invoice_pdf_url = reverse('generate_invoice_pdf', args=[self.invoice.pk])
    
    def test_generate_invoice_pdf_unauthenticated(self):
        """Test that unauthenticated users cannot generate invoice PDFs"""
        response = self.client.get(self.generate_invoice_pdf_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    @patch('hsabackend.utils.pdf_helpers.generate_pdf')
    def test_generate_invoice_pdf_authenticated(self, mock_generate_pdf):
        """Test that authenticated users can generate invoice PDFs"""
        # Mock the generate_pdf function to return a simple response
        mock_generate_pdf.return_value = "PDF content"
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.generate_invoice_pdf_url)
        
        # Check that the view called generate_pdf with the correct arguments
        mock_generate_pdf.assert_called_once()
        args, kwargs = mock_generate_pdf.call_args
        self.assertEqual(kwargs['job_id'], str(self.invoice.pk))
        self.assertEqual(kwargs['type_enum'], "invoice")
        
        # Check that the response is what we expect
        self.assertEqual(response, "PDF content")
    
    def test_generate_invoice_pdf_nonexistent_invoice(self):
        """Test generating a PDF for a nonexistent invoice"""
        self.client.force_authenticate(user=self.user)
        
        # Try to generate a PDF for a nonexistent invoice
        nonexistent_url = reverse('generate_invoice_pdf', args=[999])
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)