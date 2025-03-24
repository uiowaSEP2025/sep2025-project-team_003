from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import patch
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from unittest import TestCase
from django.contrib.auth.models import User
from hsabackend.views.generate_invoice_pdf_view import generate_pdf, generate_pdf_customer_org_header, add_total_and_disclaimer
from rest_framework import status
from hsabackend.models.organization import Organization
from decimal import Decimal

class PdfAPITest(APITestCase):
    def test_api_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/generate/invoice/1')
        request.user = mock_user  
        response = generate_pdf(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.generate_invoice_pdf_view.Organization.objects.get')
    @patch('hsabackend.views.generate_invoice_pdf_view.Invoice.objects.select_related')
    def test_api_not_found(self, filter, org):
        org.return_value = Organization()
        select_related = Mock()
        filter.return_value = select_related
        filter_mock = Mock()
        filter_mock.exists.return_value = False
        select_related.filter.return_value = filter_mock

        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        factory = APIRequestFactory()
        request = factory.get('/api/generate/invoice/1')
        request.user = mock_user  
        response = generate_pdf(request, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.generate_invoice_pdf_view.generate_pdf_customer_org_header')
    @patch('hsabackend.views.generate_invoice_pdf_view.generate_global_jobs_table')
    @patch('hsabackend.views.generate_invoice_pdf_view.add_total_and_disclaimer')
    @patch('hsabackend.views.generate_invoice_pdf_view.generate_table_for_specific_job')
    @patch('hsabackend.views.generate_invoice_pdf_view.Organization.objects.get')
    @patch('hsabackend.views.generate_invoice_pdf_view.Invoice.objects.select_related')
    def test_ok(self, filter, org, specific_jobs, total_disclaimer, global_jobs_table, org_header):
        org.return_value = Organization()
        select_related = Mock()
        filter.return_value = select_related
        filter_mock = MagicMock()
        filter_mock.exists.return_value = True
        select_related.filter.return_value = filter_mock

        filter_mock.__getitem__.side_effect = lambda x: Mock()

        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        global_jobs_table.return_value = ([1,2,3],2)

        factory = APIRequestFactory()
        request = factory.get('/api/generate/invoice/1')
        request.user = mock_user  
        response = generate_pdf(request, 1)

        assert response.status_code == status.HTTP_200_OK

class HelperTests(TestCase):
    
    def test_generate_pdf_customer_org_header(self):
        # Arrange
        mock_pdf = Mock()
        mock_org = Mock()
        mock_invoice = Mock()

        # Set up mock data
        mock_org.org_name = "Test Organization"
        mock_org.org_email = "org@example.com"
        mock_org.org_phone = "1234567890"

        mock_invoice.pk = 12345
        mock_invoice.customer.last_name = "Doe"
        mock_invoice.customer.first_name = "John"
        mock_invoice.customer.email = "john.doe@example.com"
        mock_invoice.customer.pk = 67890
        mock_invoice.issuance_date = "2023-10-01"
        mock_invoice.due_date = "2023-10-15"
        mock_pdf.w = 2

        # Act
        generate_pdf_customer_org_header(mock_pdf, mock_org, mock_invoice)

        # Assert
        # Check that the correct methods were called with the correct arguments
        mock_pdf.set_auto_page_break.assert_called_once_with(auto=True, margin=15)
        mock_pdf.set_font.assert_called_once_with("Times", size=12)

        # Check the calls to `cell` and `ln` methods
        mock_pdf.cell.assert_any_call(mock_pdf.w / 2 - 10, 10, "INVOICE ID: 12345", align="L")
        mock_pdf.cell.assert_any_call(mock_pdf.w / 2 - 10, 10, "Test Organization", align="R")
        mock_pdf.cell.assert_any_call(mock_pdf.w / 2 - 10, 10, "Doe, John", align="L")
        mock_pdf.cell.assert_any_call(mock_pdf.w / 2 - 10, 10, "org@example.com", align="R")
        mock_pdf.cell.assert_any_call(mock_pdf.w / 2 - 10, 10, "john.doe@example.com", align="L")
        mock_pdf.cell.assert_any_call(mock_pdf.w / 2 - 10, 10, "(123) - 456 - 7890", align="R")
        mock_pdf.cell.assert_any_call(mock_pdf.w / 2 - 10, 10, "CUSTOMER ID: 67890", align="L")
        mock_pdf.cell.assert_any_call(mock_pdf.w / 2 - 10, 10, "ISSUANCE DATE: 2023-10-01", align="L")
        mock_pdf.cell.assert_any_call(mock_pdf.w / 2 - 10, 10, "DUE DATE: 2023-10-15", align="L")

    def test_add_total_and_disclaimer(self):

        disclaimer_text = """
        *Disclaimer: The information on this invoice has been consolidated from reliable sources; however, 
        it may not always be entirely accurate. If you notice any discrepancies, please address them directly 
        with the handyman listed on the invoice. You remain responsible for paying the original agreed-upon 
        amount, regardless of any errors or inconsistencies in this document.
        """


        # Arrange
        mock_pdf = Mock()
        mock_org_name = "Test Organization"
        mock_total = Decimal(100.50)

        # Act
        add_total_and_disclaimer(mock_pdf, mock_total, mock_org_name)

        # Assert
        # Check that the correct methods were called with the correct arguments
        mock_pdf.ln.assert_any_call(5)
        mock_pdf.set_left_margin.assert_any_call(10)
        mock_pdf.multi_cell.assert_any_call(
            0, 
            text=f"Please make payment to {mock_org_name} for amount $100.50*", 
            align="L"
        )
        mock_pdf.set_left_margin.assert_any_call(0)
        mock_pdf.set_y.assert_any_call(-40)
        mock_pdf.multi_cell.assert_any_call(0, text=disclaimer_text, align="C")