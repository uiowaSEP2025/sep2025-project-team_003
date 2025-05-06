import unittest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from fpdf import FPDF
from hsabackend.models.job import Job
from hsabackend.utils.string_formatters import format_currency
from hsabackend.utils.pdf_utils import get_job_detailed_table  # Replace with actual module path


class TestGetJobDetailedTable(unittest.TestCase):

    @patch("hsabackend.models.job_material.JobMaterial.objects.filter")
    @patch("hsabackend.models.job_service.JobService.objects.select_related")
    def test_get_job_detailed_table(self, mock_select_related, mock_material_filter):
        # Setup mocks
        mock_pdf = MagicMock(spec=FPDF)
        table_ctx_mgr = MagicMock()
        tbl = MagicMock()
        row = MagicMock()

        # Configure the mock PDF table context manager
        table_ctx_mgr.__enter__.return_value = tbl
        table_ctx_mgr.__exit__.return_value = False
        mock_pdf.table.return_value = table_ctx_mgr
        tbl.row.return_value = row

        # Dummy Job object
        job = Job(hourly_rate=Decimal("100.00"), minutes_worked=120, flat_fee=Decimal("50.00"))

        # Dummy JobService info
        svc_mock = MagicMock()
        svc_mock.get_service_info_for_detailed_invoice.return_value = {
            "service name": "Consulting",
            "service description": "IT consultation"
        }
        mock_select_related.return_value.filter.return_value = [svc_mock]

        # Dummy JobMaterial info
        mat_mock = MagicMock()
        mat_mock.invoice_material_row.return_value = {
            "material name": "Cable",
            "per unit": Decimal("10.00"),
            "units used": 3,
            "total": Decimal("30.00"),
        }
        mock_material_filter.return_value = [mat_mock]

        # Run the function
        get_job_detailed_table(mock_pdf, job)

        # Assert table and row calls were made
        self.assertTrue(mock_pdf.table.called)
        self.assertTrue(tbl.row.called)
        self.assertTrue(row.cell.called)
        self.assertTrue(mock_pdf.ln.called)

        # Assert specific values were formatted and used
        labor_cost = job.hourly_rate * (Decimal(job.minutes_worked) / Decimal(60)) + job.flat_fee
        grand_total = labor_cost + Decimal("30.00")

        row.cell.assert_any_call(format_currency(labor_cost))
        row.cell.assert_any_call(format_currency(grand_total))