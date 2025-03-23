from unittest.mock import Mock
from unittest.mock import patch
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from unittest import TestCase
from django.contrib.auth.models import User
from hsabackend.views.generate_invoice_pdf_view import generate_pdf
from rest_framework import status

class PdfAPITest(APITestCase):
    def test_api_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/customers?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = generate_pdf(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_api_not_found(self):
        pass

    def test_ok(self):
        pass

class HelperTests(TestCase):
    pass
