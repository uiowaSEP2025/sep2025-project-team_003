from django.contrib.auth.models import User

from hsabackend.models.customer import Customer
from hsabackend.models.invoice import Invoice
from hsabackend.models.organization import Organization
from hsabackend.views.generate_invoice_pdf_view import generate_pdf, add_job_header, add_total_and_disclaimer, generate_global_jobs_table, generate_pdf_customer_org_header
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from unittest.mock import Mock, patch, MagicMock
from unittest import TestCase
from decimal import Decimal

class GenerateInvoiceTest(APITestCase):

    @patch('hsabackend.views.generate_invoice_pdf_view.Invoice.objects.select_related')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_no_invoice(self, obj, inv):
        mock_user = Mock()
        mock_user.is_authenticated = True

        org = Mock()
        org.is_onboarding = False
        obj.return_value = org

        factory = APIRequestFactory()
        request = factory.get('/api/request/genhtml/42')
        request.user = mock_user

        mock_qs = Mock()
        mock_qs.exists.return_value = False
        f = Mock()
        inv.return_value = f
        f.filter.return_value = mock_qs
        
        response = generate_pdf(request, 42)

        assert response.status_code == 404

        
    @patch('hsabackend.views.generate_invoice_pdf_view.add_total_and_disclaimer')
    @patch('hsabackend.views.generate_invoice_pdf_view.generate_global_jobs_table')
    @patch('hsabackend.views.generate_invoice_pdf_view.generate_pdf_customer_org_header')
    @patch('hsabackend.views.generate_invoice_pdf_view.Invoice.objects.select_related')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_ok(self, obj, inv, k,j, d):
        mock_user = Mock()
        mock_user.is_authenticated = True

        org = Mock()
        org.is_onboarding = False
        obj.return_value = org

        factory = APIRequestFactory()
        request = factory.get('/api/request/genhtml/42')
        request.user = mock_user
        j.return_value = ([],1)
        mock_qs = MagicMock()
        mock_qs.exists.return_value = True
        f = MagicMock()
        inv.return_value = f
        f.filter.return_value = mock_qs
        
        response = generate_pdf(request, 42)

        assert response.status_code == 200

class BSCov(TestCase):
    
    @patch('hsabackend.views.generate_invoice_pdf_view.format_date_to_iso_string')
    def test_add_job_header(self, p):
        pdf = MagicMock()
        job = MagicMock()
        job.pk = 123
        job.truncated_job_desc = "Fix plumbing"
        job.start_date = "2025-05-01"
        job.full_display_address = "123 Main St, City, Country"

        p.return_value =  "2025-05-01"

        add_job_header(pdf, job)

        pdf.set_font.assert_any_call("Arial", size=12, style='B')
        pdf.set_xy.assert_any_call(10, 20)
        pdf.cell.assert_any_call(10, 10, "Job 123 - Fix plumbing", ln=True)

        pdf.set_font.assert_any_call("Arial", size=10)
        pdf.set_xy.assert_any_call(10, 30)
        pdf.cell.assert_any_call(10, 10, "Start Date: 2025-05-01", ln=True)

        pdf.set_xy.assert_any_call(10, 40)
        pdf.cell.assert_any_call(10, 10, "Address: 123 Main St, City, Country", ln=True)

        pdf.ln.assert_called_with(5)

    def test_add_total_and_disclaimer(self):
        self.test_user = User.objects.create_user(
            username='testuser33',
            email='testuser33@example.com',
            password='testpassword'
        )

        self.test_organization = Organization.objects.create(
            org_name='Test Organization',
            org_email='testorg@example.com',
            org_city='Test City',
            org_requestor_state='Iowa',  # Using a valid state as per the validator
            org_requestor_zip='12345',
            org_requestor_address='123 Test St',
            org_phone='1234567890',
            org_owner_first_name='Test',
            org_owner_last_name='Owner',
            owning_User=self.test_user,
            is_onboarding=False,
        )

        self.test_customer = Customer.objects.create(
            first_name="First Cus",
            last_name="Last Cus",
            email="cus@example.com",
            phone_no=9876543210,
            organization=self.test_organization,
        )

        self.test_invoice = Invoice.objects.create(
            issuance_date="2025-05-04",
            due_date="2025-05-14",
            status="create",
            tax=0.02,
            customer=self.test_customer,
            payment_url="https://www.paypal.com"
        )

        pdf = MagicMock()
        total = Decimal('123.45')
        org_name = "example org"

        add_total_and_disclaimer(pdf, total, org_name, self.test_invoice)

        expected_payment_text = f"Please make payment to Example Org for amount $123.45*"

        pdf.ln.assert_any_call(5)
        pdf.set_left_margin.assert_any_call(10)
        pdf.multi_cell.assert_any_call(0, text=expected_payment_text, align="L")
        pdf.set_left_margin.assert_any_call(0)
        pdf.set_y.assert_called_with(-40)
        self.assertTrue(any("Disclaimer" in call.kwargs['text'] for call in pdf.multi_cell.mock_calls))

    @patch("hsabackend.views.generate_invoice_pdf_view.Job.objects.filter")
    @patch("hsabackend.views.generate_invoice_pdf_view.format_date_to_iso_string")
    def test_generate_global_jobs_table_basic(self, iso, jf):
        # Create a mock invoice
        invoice = MagicMock()
        invoice.tax = Decimal("10")  # 10%

        # Create mock jobs
        job1 = MagicMock()
        job1.pk = 1
        job1.start_date = "2024-01-01"
        job1.truncated_job_desc = "Fix sink"
        job1.full_display_address = "123 Main St"
        job1.total_cost = Decimal("100.00")

        job2 = MagicMock()
        job2.pk = 2
        job2.start_date = "2024-01-02"
        job2.truncated_job_desc = "Paint house"
        job2.full_display_address = "456 Oak St"
        job2.total_cost = Decimal("200.00")

        iso.return_value = "2025-05-01"

        jf.return_value = [job1, job2]

        # Mock FPDF and table behavior
        mock_pdf = MagicMock()
        mock_table_ctx = MagicMock()
        mock_row = MagicMock()
        mock_pdf.table.return_value.__enter__.return_value.row.return_value = mock_row

        # Call the function
        jobs_list, total_with_tax = generate_global_jobs_table(mock_pdf, invoice)

        # Assertions
        self.assertEqual(jobs_list, [job1, job2])
        expected_total = Decimal("300.00") + (Decimal("300.00") * Decimal("0.10"))
        self.assertEqual(total_with_tax, expected_total)

        # Verify table calls
        self.assertTrue(mock_pdf.table.called)
        self.assertEqual(mock_row.cell.call_count, 35)  # 2 jobs + 3 summary rows
    
    def test_generate_pdf_customer_org_header(self):
        # Create a mock FPDF object
        mock_pdf = Mock()
        mock_pdf.w = 210  # Typical A4 page width in mm

        # Create mock organization
        org = Mock()
        org.org_name = "example org"
        org.org_email = "org@example.com"
        org.org_phone = "1234567890"

        # Create mock customer
        customer = Mock()
        customer.first_name = "Jane"
        customer.last_name = "Doe"
        customer.email = "jane.doe@example.com"
        customer.pk = 42

        # Create mock invoice
        invoice = Mock()
        invoice.pk = 1001
        invoice.customer = customer
        invoice.issuance_date = "2023-01-01"
        invoice.due_date = "2023-01-15"


        # Call the function
        generate_pdf_customer_org_header(mock_pdf, org, invoice)

        # Basic assertions to ensure .cell and .ln were called
        self.assertTrue(mock_pdf.cell.called)
        self.assertTrue(mock_pdf.ln.called)
        self.assertTrue(mock_pdf.set_auto_page_break.called)
        self.assertTrue(mock_pdf.set_font.called)

        # Optional: check some specific calls
        mock_pdf.cell.assert_any_call(95.0, 10, "INVOICE ID: 1001", align="L")
        mock_pdf.cell.assert_any_call(95.0, 10, "Example Org", align="R")