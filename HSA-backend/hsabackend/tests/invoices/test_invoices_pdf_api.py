from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.utils.pdf_helpers import generate_pdf


class InvoicesPDFAPITest(BaseTestCase):
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
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
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
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        select_related = Mock()
        filter.return_value = select_related
        filter_mock = MagicMock()
        filter_mock.exists.return_value = True
        select_related.filter.return_value = filter_mock

        filter_mock.__getitem__.side_effect = lambda x: Mock()

        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        global_jobs_table.return_value = ([1, 2, 3], 2)

        factory = APIRequestFactory()
        request = factory.get('/api/generate/invoice/1')
        request.user = mock_user
        response = generate_pdf(request, 1)

        assert response.status_code == status.HTTP_200_OK
