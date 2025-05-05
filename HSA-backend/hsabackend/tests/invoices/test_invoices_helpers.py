from decimal import Decimal
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from hsabackend.tests import BaseTestCase
from hsabackend.utils.pdf_helpers import generate_pdf_customer_org_header, add_total_and_disclaimer, \
    generate_global_jobs_table, generate_table_for_specific_job


class InvoicesHelpersTest(BaseTestCase):

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

    @patch('hsabackend.views.generate_invoice_pdf_view.Quote.objects.select_related')
    def test_generate_global_jobs_table_without_discount(self, mock_select_related):
        pdf = MagicMock()
        invoice = MagicMock()
        invoice.tax = Decimal('0.10')
        m1 = Mock()
        m2 = Mock()
        m3 = Mock()
        m4 = MagicMock()

        q1 = Mock()
        q2 = Mock()
        q1.jobID.pk = 1
        q1.geerate_invoice_global_table_json.return_value = {
            "Date": "2025-03-23",
            "Job Description": "Repair and maintenance of HVAC system",
            "Address": "123 Main St, Springfield, IL, 62704",
            "Total Undiscounted": Decimal(300.00),
            "Discount Percent": Decimal(0.0)}

        q2.jobID.pk = 2
        q2.geerate_invoice_global_table_json.return_value = {
            "Date": "2025-03-23",
            "Job Description": "Repair and maintenance of HVAC system",
            "Address": "123 Main St, Springfield, IL, 62704",
            "Total Undiscounted": Decimal(300.00),
            "Discount Percent": Decimal(0.0)}

        m4.__iter__.return_value = [q1, q2]
        # Mock the queryset
        mock_select_related.return_value = m1
        m1.select_related.return_value = m2
        m2.filter.return_value = m3
        m3.order_by.return_value = m4

        m4.__len__.return_value = 2

        job_ids, total_amount = generate_global_jobs_table(pdf, invoice)
        self.assertEqual(job_ids, [1, 2])
        self.assertEqual(total_amount, Decimal('660.00'))  # 300 + 10% tax

        # Check if the PDF table was populated correctly
        self.assertEqual(pdf.table.call_count, 1)

    @patch('hsabackend.views.generate_invoice_pdf_view.Quote.objects.select_related')
    def test_generate_global_jobs_table_with_discount(self, mock_select_related):
        pdf = MagicMock()
        invoice = MagicMock()
        invoice.tax = Decimal('0.10')
        m1 = Mock()
        m2 = Mock()
        m3 = Mock()
        m4 = MagicMock()

        q1 = Mock()
        q2 = Mock()
        q1.jobID.pk = 1
        q1.geerate_invoice_global_table_json.return_value = {
            "Date": "2025-03-23",
            "Job Description": "Repair and maintenance of HVAC system",
            "Address": "123 Main St, Springfield, IL, 62704",
            "Total Undiscounted": Decimal(300.00),
            "Discount Percent": Decimal(0.0)}

        q2.jobID.pk = 2
        q2.geerate_invoice_global_table_json.return_value = {
            "Date": "2025-03-23",
            "Job Description": "Repair and maintenance of HVAC system",
            "Address": "123 Main St, Springfield, IL, 62704",
            "Total Undiscounted": Decimal(300.00),
            "Discount Percent": Decimal(10.0)}

        m4.__iter__.return_value = [q1, q2]
        # Mock the queryset
        mock_select_related.return_value = m1
        m1.select_related.return_value = m2
        m2.filter.return_value = m3
        m3.order_by.return_value = m4

        m4.__len__.return_value = 2

        job_ids, total_amount = generate_global_jobs_table(pdf, invoice)
        self.assertEqual(job_ids, [1, 2])
        self.assertEqual(total_amount, Decimal('627.00'))  # 5% discount 10% tax

        # Check if the PDF table was populated correctly
        self.assertEqual(pdf.table.call_count, 1)

    @patch('hsabackend.views.generate_invoice_pdf_view.JobService.objects.select_related')
    @patch('hsabackend.views.generate_invoice_pdf_view.JobMaterial.objects.filter')
    def test_generate_table_for_specific_job(self, mock_material_filter, mock_service_select):
        # Setup PDF mock
        pdf = MagicMock()
        pdf.table.return_value.__enter__.return_value = MagicMock()

        # Mock services data
        service1 = Mock()
        service1.get_service_info_for_detailed_invoice.return_value = {
            "service name": "Service 1",
            "service description": "Description 1"
        }
        service2 = Mock()
        service2.get_service_info_for_detailed_invoice.return_value = {
            "service name": "Service 2",
            "service description": "Description 2"
        }

        # Mock materials data
        material1 = Mock()
        material1.invoice_material_row.return_value = {
            "material name": "Material 1",
            "per unit": Decimal('10.00'),
            "units used": 2,
            "total": Decimal('20.00')
        }
        material2 = Mock()
        material2.invoice_material_row.return_value = {
            "material name": "Material 2",
            "per unit": Decimal('15.00'),
            "units used": 1,
            "total": Decimal('15.00')
        }

        # Configure mocks
        mock_service_select.return_value.filter.return_value = [service1, service2]
        mock_material_filter.return_value = [material1, material2]

        # Call the function
        generate_table_for_specific_job(pdf, jobid=1, num_jobs=3, idx=0)

        # Assertions
        # Check PDF methods were called
        pdf.set_x.assert_called_once_with(10)
        pdf.multi_cell.assert_called_once_with(100, text="Job #1 of 3", align="L")
        pdf.ln.assert_called_once_with(5)

        # Check table creation (should be called twice - once for services, once for materials)
        self.assertEqual(pdf.table.call_count, 2)

        # Get the table context manager
        table_mock = pdf.table.return_value.__enter__.return_value

        # Check service table rows
        service_header = table_mock.row.call_args_list[0]
        self.assertEqual(service_header.kwargs, {})