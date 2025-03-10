from rest_framework.test import APITestCase
from unittest.mock import Mock, patch, MagicMock
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from hsabackend.views.invoices import getInvoices
from rest_framework import status

class InvoiceViewTest(APITestCase):

    def test_get_invoice_table_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = getInvoices(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_get_invoice_table_no_pagesize(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search&&offset=0')
        request.user = mock_user  
        mock_org = Mock()
        org.return_value = mock_org
        response = getInvoices(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_get_invoice_table_pagesize_string(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search&&offset=0&pagesize=ae')
        request.user = mock_user  
        mock_org = Mock()
        org.return_value = mock_org
        response = getInvoices(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    @patch('hsabackend.views.invoices.Invoice.objects.select_related')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_get_invoice_table_ok(self, org, invoice):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search&&offset=0&pagesize=2')
        request.user = mock_user  
        mock_org = Mock()
        org.return_value = mock_org

        mock_select = Mock()
        invoice.return_value = mock_select
        mock_filtered = MagicMock()
        mock_select.filter.return_value = mock_filtered

        response = getInvoices(request)
        
        assert response.status_code == status.HTTP_200_OK