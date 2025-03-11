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

    @patch('hsabackend.views.quotes.Organization.objects.get')
    def test_get_quotes_by_cust_id_invalid_page_size(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org.return_value = Organization()
        factory = APIRequestFactory()
        
        request = factory.get('api/get/quotesforinvoice/customer/1?search&pagesize=a&offset=0')
        request.user = mock_user  
        response = getQuotesForInvoiceByCustomer(request,1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.quotes.Customer.objects.filter')
    @patch('hsabackend.views.quotes.Organization.objects.get')
    def test_get_quotes_by_cust_id_cust_not_found(self, org, cust):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org.return_value = Organization()
        factory = APIRequestFactory()

        custqs = Mock()
        custqs.exists.return_value = False
        cust.return_value = custqs
        
        request = factory.get('api/get/quotesforinvoice/customer/1?search&pagesize=10&offset=0')
        request.user = mock_user  
        response = getQuotesForInvoiceByCustomer(request,1)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.quotes.Quote.objects.filter')
    @patch('hsabackend.views.quotes.Quote.objects.select_related')
    @patch('hsabackend.views.quotes.Customer.objects.filter')
    @patch('hsabackend.views.quotes.Organization.objects.get')
    def test_get_quotes_by_cust_id_ok(self, org, cust, quote, quote_count):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org.return_value = Organization()
        factory = APIRequestFactory()

        custqs = Mock()
        custqs.exists.return_value = True
        cust.return_value = custqs
        
        quoteqs1 = Mock(name='q1')
        quote.return_value = quoteqs1

        quoteqs2 = Mock(name='q2')
        quoteqs1.select_related.return_value = quoteqs2

        filtered_quotes = MagicMock(name='magic')
        quoteqs2.filter.return_value = filtered_quotes

        quote_count.return_value = Mock()

        request = factory.get('api/get/quotesforinvoice/customer/1?search&pagesize=10&offset=0')
        request.user = mock_user  
        response = getQuotesForInvoiceByCustomer(request,1)
        assert response.status_code == status.HTTP_200_OK
