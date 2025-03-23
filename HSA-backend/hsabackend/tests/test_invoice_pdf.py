from unittest.mock import Mock
from unittest.mock import patch
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from unittest import TestCase
from django.contrib.auth.models import User
from hsabackend.views.generate_invoice_pdf_view import generate_pdf
from rest_framework import status
from hsabackend.models.organization import Organization

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

    def test_ok(self):
        pass

class HelperTests(TestCase):
    pass
