from unittest.mock import MagicMock, Mock, patch
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from hsabackend.models.organization import Organization
from rest_framework.test import APITestCase
from rest_framework import status
from hsabackend.views.quotes import getQuotesForInvoiceByCustomer

class testQuotesView(APITestCase):
    def test_get_quotes_by_cust_id_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('api/get/quotesforinvoice/customer/1?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = getQuotesForInvoiceByCustomer(request,1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.quotes.Organization.objects.get')
    def test_get_quotes_by_cust_id_missing_pagesize(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org.return_value = Organization()
        factory = APIRequestFactory()
        
        request = factory.get('api/get/quotesforinvoice/customer/1?search&offset=0')
        request.user = mock_user  
        response = getQuotesForInvoiceByCustomer(request,1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_quotes_by_cust_id_invalid_page_size(self):
        pass

    def test_get_quotes_by_cust_id_cust_not_found(self):
        pass

    def test_get_quotes_by_cust_id_ok(self):
        pass