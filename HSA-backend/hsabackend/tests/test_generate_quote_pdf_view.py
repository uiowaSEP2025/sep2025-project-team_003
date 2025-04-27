from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from decimal import Decimal
from datetime import date
from hsabackend.models.organization import Organization
from hsabackend.models.customer import Customer
from hsabackend.models.job import Job

class GenerateQuotePDFViewTest(TestCase):
    """Test cases for the Generate Quote PDF view"""
    
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
        
        # Create a job
        self.job = Job.objects.create(
            job_status="created",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 31),
            description="Test Job Description",
            organization=self.organization,
            customer=self.customer,
            job_city="Test City",
            job_state="TS",
            job_zip="12345",
            job_address="456 Test Ave"
        )
        
        # Set up the API client
        self.client = APIClient()
        
        # URLs
        self.generate_quote_pdf_url = reverse('generate_quote_pdf', args=[self.job.pk])
        self.send_quote_pdf_url = reverse('send_quote_pdf_to_customer_email', args=[self.job.pk])
    
    def test_generate_quote_pdf_unauthenticated(self):
        """Test that unauthenticated users cannot generate quote PDFs"""
        response = self.client.get(self.generate_quote_pdf_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    @patch('hsabackend.utils.pdf_helpers.generate_pdf')
    def test_generate_quote_pdf_authenticated(self, mock_generate_pdf):
        """Test that authenticated users can generate quote PDFs"""
        # Mock the generate_pdf function to return a simple response
        mock_generate_pdf.return_value = "PDF content"
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.generate_quote_pdf_url)
        
        # Check that the view called generate_pdf with the correct arguments
        mock_generate_pdf.assert_called_once()
        args, kwargs = mock_generate_pdf.call_args
        self.assertEqual(kwargs['job_id'], str(self.job.pk))
        self.assertEqual(kwargs['type_enum'], "quote")
        
        # Check that the response is what we expect
        self.assertEqual(response, "PDF content")
    
    def test_generate_quote_pdf_nonexistent_job(self):
        """Test generating a PDF for a nonexistent job"""
        self.client.force_authenticate(user=self.user)
        
        # Try to generate a PDF for a nonexistent job
        nonexistent_url = reverse('generate_quote_pdf', args=[999])
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_send_quote_pdf_unauthenticated(self):
        """Test that unauthenticated users cannot send quote PDFs"""
        response = self.client.post(self.send_quote_pdf_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    @patch('hsabackend.views.generate_quote_pdf_view.EmailMultiAlternatives')
    @patch('hsabackend.views.generate_quote_pdf_view.FPDF')
    def test_send_quote_pdf_authenticated(self, mock_fpdf, mock_email):
        """Test that authenticated users can send quote PDFs"""
        # Mock the FPDF class and its methods
        mock_pdf_instance = MagicMock()
        mock_fpdf.return_value = mock_pdf_instance
        
        # Mock the EmailMultiAlternatives class and its methods
        mock_email_instance = MagicMock()
        mock_email.return_value = mock_email_instance
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.send_quote_pdf_url)
        
        # Check that the view created a PDF
        mock_fpdf.assert_called_once()
        
        # Check that the view sent an email
        mock_email.assert_called_once()
        mock_email_instance.send.assert_called_once()
        
        # Check that the response is what we expect
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Quote PDF sent to", response.data["message"])
    
    def test_send_quote_pdf_nonexistent_job(self):
        """Test sending a PDF for a nonexistent job"""
        self.client.force_authenticate(user=self.user)
        
        # Try to send a PDF for a nonexistent job
        nonexistent_url = reverse('send_quote_pdf_to_customer_email', args=[999])
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)