from django.test import TestCase
from decimal import Decimal
from hsabackend.models.job import Job
from unittest.mock import Mock, patch
from hsabackend.models.organization import Organization
from hsabackend.models.customer import Customer
from hsabackend.models.invoice import Invoice

class JobModelCalculationTestCase(TestCase):

    def setUp(self):
        # Create a mock for the related fields (organization, customer, invoice)
        self.organization = Organization()
        self.organization.name = "Test Organization"
        
        self.customer = Customer()
        self.customer.first_name = "John"
        self.customer.last_name = "Doe"
        
        self.invoice = Invoice()
        self.invoice.amount = Decimal('100.00')

        # Create a Job instance with necessary fields
        self.job = Job(
            job_status="created",
            start_date="2025-05-06",  # Example date
            end_date="2025-05-06",    # Example date
            description="Test job description",
            organization=self.organization,
            customer=self.customer,
            requestor_city="Test City",
            requestor_state="TS",
            requestor_zip="12345",
            requestor_address="123 Test St",
            flat_fee=Decimal('50.00'),
            hourly_rate=Decimal('25.00'),
            minutes_worked=120,
            invoice=self.invoice
        )

        # Create a mock for JobMaterial cost calculation
        self.job_material = Mock()
        self.job_material.units_used = 5
        self.job_material.price_per_unit = Decimal('10.00')

        # Mock the JobMaterial query to return a list with the mock object
        self.job_materials_mock = [self.job_material]

    def test_full_display_address(self):
        """Test that the full_display_address property returns the correct formatted address."""
        expected_address = "123 Test St, Test City, TS, 12345"
        self.assertEqual(self.job.full_display_address, expected_address)

    def test_truncated_job_desc(self):
        """Test that the truncated_job_desc property returns the correct truncated description."""
        # If the description is greater than 50 characters, it should truncate and add "..."
        long_description = "Test job description that exceeds fifty characters hiiiiiiiiiii"
        job_with_long_desc = Job(
            job_status="created",
            start_date="2025-05-06",  
            end_date="2025-05-06",
            description=long_description,
            organization=self.organization,
            customer=self.customer,
            requestor_city="Test City",
            requestor_state="TS",
            requestor_zip="12345",
            requestor_address="123 Test St",
            flat_fee=Decimal('50.00'),
            hourly_rate=Decimal('25.00'),
            minutes_worked=120,
            invoice=self.invoice
        )
        expected_truncated_desc = "Test job description that exceeds fifty characters..."
        self.assertEqual(job_with_long_desc.truncated_job_desc, expected_truncated_desc)

        # If the description is less than or equal to 50 characters, it should return as-is
        short_description = "Short desc"
        job_with_short_desc = Job(
            job_status="created",
            start_date="2025-05-06",  
            end_date="2025-05-06",
            description=short_description,
            organization=self.organization,
            customer=self.customer,
            requestor_city="Test City",
            requestor_state="TS",
            requestor_zip="12345",
            requestor_address="123 Test St",
            flat_fee=Decimal('50.00'),
            hourly_rate=Decimal('25.00'),
            minutes_worked=120,
            invoice=self.invoice
        )
        self.assertEqual(job_with_short_desc.truncated_job_desc, short_description)

    @patch('hsabackend.models.job.JobMaterial.objects.filter')
    def test_total_cost(self, jm):
        mock_jm_1 = Mock()
        mock_jm_1.units_used = 10   
        mock_jm_1.price_per_unit = Decimal('19.99')
        mock_jm_2 = Mock()
        mock_jm_2.units_used = 15
        mock_jm_2.price_per_unit = Decimal('19.99')
        job = job = Job(
            job_status="created",
            start_date="2025-05-01",
            end_date="2025-05-10",
            description="Fix plumbing issue in basement",
            organization=Organization(),
            customer=Customer(),
            requestor_city="Los Angeles",
            requestor_state="CA",
            requestor_zip="90001",
            requestor_address="1234 Sunset Blvd",
            flat_fee=Decimal("200.00"),
            hourly_rate=Decimal("75.00"),
            minutes_worked=90,
        )
        
        assert job.total_cost == 312.50
