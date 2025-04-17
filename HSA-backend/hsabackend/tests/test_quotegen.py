import io
import os
import unittest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APITestCase

from hsabackend.views.generate_quote_pdf_view import (
    generate_pdf_customer_org_header,
    generate_table_for_specific_job,
    generate_signature_page,
    generate_quote_pdf,
    send_quote_pdf_to_customer_email,
)


class HelperTests(unittest.TestCase):
    def test_generate_pdf_customer_org_header(self):
        pdf = Mock()
        pdf.w = 120
        org = Mock(org_name="test org", org_email="org@example.com", org_phone="5551234567")
        invoice = Mock(pk=99)
        invoice.customer.last_name = "Smith"
        invoice.customer.first_name = "Alice"
        invoice.customer.email = "alice@example.com"
        invoice.customer.pk = 7
        invoice.start_date = "2025-02-02"
        invoice.end_date = None

        generate_pdf_customer_org_header(pdf, org, invoice)

        pdf.set_auto_page_break.assert_called_once_with(auto=True, margin=15)
        pdf.set_font.assert_called_once_with("Times", size=12)
        # header cells
        # customer name and email
        self.assertGreaterEqual(pdf.ln.call_count, 1)

    @patch('hsabackend.views.generate_quote_pdf_view.JobService')
    @patch('hsabackend.views.generate_quote_pdf_view.JobMaterial')
    def test_generate_table_for_specific_job(self, mock_mat, mock_svc):
        pdf = Mock()
        # simulate table context manager
        table_cm = MagicMock()
        table = table_cm.__enter__.return_value
        pdf.table.return_value = table_cm

        # services
        svc1 = Mock(get_service_info_for_detailed_invoice=Mock(return_value={
            "service name": "SV1", "service description": "Desc1"
        }))
        svc2 = Mock(get_service_info_for_detailed_invoice=Mock(return_value={
            "service name": "SV2", "service description": "Desc2"
        }))
        mock_svc.objects.select_related.return_value.filter.return_value = [svc1, svc2]

        # materials
        mat1 = Mock(invoice_material_row=Mock(return_value={
            "material name": "M1", "per unit": Decimal('2.50'), "units used": 2, "total": Decimal('5.00')
        }))
        mat2 = Mock(invoice_material_row=Mock(return_value={
            "material name": "M2", "per unit": Decimal('3.00'), "units used": 1, "total": Decimal('3.00')
        }))
        mock_mat.objects.filter.return_value = [mat1, mat2]

        generate_table_for_specific_job(pdf, jobid=1, num_jobs=1, idx=0)

        # two separate tables
        self.assertEqual(pdf.table.call_count, 2)
        # header row called at least once per table
        self.assertGreaterEqual(table.row.call_count, 2)
        # ensure ln called after each table
        self.assertGreaterEqual(pdf.ln.call_count, 1)

    def test_generate_signature_page(self):
        pdf = Mock()
        pdf.l_margin = 20
        pdf.r_margin = 20
        pdf.w = 200
        pdf.get_y.return_value = 50

        generate_signature_page(pdf)

        pdf.add_page.assert_called_once()
        pdf.set_font.assert_called_once_with("Times", size=12)
        pdf.multi_cell.assert_called_once()
        pdf.cell.assert_called_once()
        pdf.line.assert_called_once()


class GenerateQuotePdfAPITests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_generate_quote_pdf_unauthenticated(self):
        request = self.factory.get('/quote/1')
        request.user = Mock(is_authenticated=False)

        resp = generate_quote_pdf(request, 1)
        self.assertIsInstance(resp, Response)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('hsabackend.views.generate_quote_pdf_view.Organization')
    @patch('hsabackend.views.generate_quote_pdf_view.Job')
    def test_generate_quote_pdf_not_found(self, mock_job, mock_org):
        request = self.factory.get('/quote/1')
        request.user = Mock(is_authenticated=True)
        mock_org.objects.get.return_value = Mock()
        empty_qs = MagicMock(exists=MagicMock(return_value=False))
        mock_job.objects.select_related.return_value.filter.return_value = empty_qs

        resp = generate_quote_pdf(request, 123)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @patch('hsabackend.views.generate_quote_pdf_view.generate_pdf_customer_org_header')
    @patch('hsabackend.views.generate_quote_pdf_view.generate_table_for_specific_job')
    @patch('hsabackend.views.generate_quote_pdf_view.generate_signature_page')
    @patch('hsabackend.views.generate_quote_pdf_view.Organization')
    @patch('hsabackend.views.generate_quote_pdf_view.Job')
    def test_generate_quote_pdf_success(self,
                                        mock_job,
                                        mock_org,
                                        mock_sig,
                                        mock_table,
                                        mock_header):
        request = self.factory.get('/quote/5')
        request.user = Mock(is_authenticated=True)
        mock_org.objects.get.return_value = Mock()
        fake_job = Mock(pk=5, customer=Mock())
        qs = MagicMock(exists=MagicMock(return_value=True))
        qs.__getitem__.return_value = fake_job
        mock_job.objects.select_related.return_value.filter.return_value = qs

        resp = generate_quote_pdf(request, 5)
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp['Content-Type'], 'application/pdf')
        self.assertIn('Content-Disposition', resp)


class SendQuotePdfEmailTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_send_quote_pdf_to_customer_email_unauth(self):
        request = self.factory.post('/quote/send/1')
        request.user = Mock(is_authenticated=False)

        resp = send_quote_pdf_to_customer_email(request, 1)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('hsabackend.views.generate_quote_pdf_view.Organization')
    @patch('hsabackend.views.generate_quote_pdf_view.Job')
    def test_send_quote_pdf_to_customer_email_not_found(self, mock_job, mock_org):
        request = self.factory.post('/quote/send/1')
        request.user = Mock(is_authenticated=True)
        mock_org.objects.get.return_value = Mock()
        # simulate DoesNotExist
        class FakeJob:
            class DoesNotExist(Exception):
                pass
        def raise_not_found(*args, **kwargs):
            raise FakeJob.DoesNotExist
        mock_job.objects.select_related.return_value.get.side_effect = raise_not_found
        mock_job.DoesNotExist = FakeJob.DoesNotExist

        resp = send_quote_pdf_to_customer_email(request, 9)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @patch('hsabackend.views.generate_quote_pdf_view.EmailMultiAlternatives')
    @patch('hsabackend.views.generate_quote_pdf_view.Organization')
    @patch('hsabackend.views.generate_quote_pdf_view.Job')
    def test_send_quote_pdf_to_customer_email_success(self, mock_job, mock_org, mock_email):
        request = self.factory.post('/quote/send/77')
        request.user = Mock(is_authenticated=True)
        mock_org.objects.get.return_value = Mock()
        cust = Mock(email="cust@example.com", first_name="Bob")
        fake_job = Mock(pk=77, customer=cust)
        mock_job.objects.select_related.return_value.get.return_value = fake_job

        # stub PDF generators
        with patch('hsabackend.views.generate_quote_pdf_view.generate_pdf_customer_org_header'):
            with patch('hsabackend.views.generate_quote_pdf_view.generate_table_for_specific_job'):
                with patch('hsabackend.views.generate_quote_pdf_view.generate_signature_page'):
                    # prepare email mock
                    email_msg = Mock(attach_alternative=Mock(), attach=Mock(), send=Mock())
                    mock_email.return_value = email_msg
                    os.environ['EMAIL_HOST_USER'] = 'no-reply@example.com'

                    resp = send_quote_pdf_to_customer_email(request, 77)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, {"message": f"Quote PDF sent to {cust.email}"})
        email_msg.send.assert_called_once()


