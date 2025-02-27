from rest_framework.test import APITestCase
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status
from hsabackend.views.requests import get_org_request_data
from hsabackend.models.organization import Organization
from django.db.models import QuerySet
from django.db.models import Q

class UserAuthViewTest(APITestCase):
    def test_get_customer_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/requests?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = get_org_request_data(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_get_request_table_data_invalid(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        factory = APIRequestFactory()
        request = factory.get('/api/get/requests?search')
        request.user = mock_user  
        response = get_org_request_data(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.requests.Request.objects.filter')
    @patch('hsabackend.views.requests.Organization.objects.get')
    def test_get_request_table_data_valid_query(self,get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        qs = MagicMock(spec=QuerySet) # needed because it's sliced in the code
        filter.return_value = qs
        

        factory = APIRequestFactory()
        request = factory.get('/api/get/requests?search=bob&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_org_request_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        qs.filter.assert_called_with(Q(name__icontains='bob')) 

    
    @patch('hsabackend.views.requests.Request.objects.filter')
    @patch('hsabackend.views.requests.Organization.objects.get')
    def test_get_request_table_data_valid_query_empty(self,get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org = Mock(spec=Organization)
        org.pk = 1
        get.return_value = org
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/requests?search&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_org_request_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        filter.assert_called_with(organization=1) 