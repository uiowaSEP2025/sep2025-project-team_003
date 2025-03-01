from rest_framework.test import APITestCase
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status
from hsabackend.views.requests import get_org_request_data, delete_request, approve_request
from hsabackend.models.organization import Organization
from django.db.models import QuerySet
from django.db.models import Q

class RequestView(APITestCase):
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

    def test_delete_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/request/1')
        request.user = mock_user  
        response = delete_request(request,1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.requests.Organization.objects.get')
    @patch('hsabackend.views.requests.Request.objects.filter')
    def test_delete_not_found(self, req, get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org = Mock(spec=Organization)
        org.pk = 1
        get.return_value = org
        req_qs = MagicMock(id="request_queryset")
        req_qs.exists.return_value = False
        req.return_value = req_qs


        factory = APIRequestFactory()
        request = factory.post('/api/delete/request/1')
        request.user = mock_user  
        response = delete_request(request,1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.requests.Organization.objects.get')
    @patch('hsabackend.views.requests.Request.objects.filter')
    def test_delete_success(self, req,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org = Mock(spec=Organization)
        org.pk = 1
        get.return_value = org
        req_qs = MagicMock(id="request_queryset")
        req_qs.exists.return_value = True
        req.return_value = req_qs

        factory = APIRequestFactory()
        request = factory.post('/api/delete/request/1')
        request.user = mock_user  
        response = delete_request(request,1)

        assert response.status_code == status.HTTP_200_OK

    def test_approve_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/approve/request/1')
        request.user = mock_user  
        response = approve_request(request,1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.requests.Organization.objects.get')
    @patch('hsabackend.views.requests.Request.objects.filter')
    def test_approve_not_exists(self,filter, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        factory = APIRequestFactory()
        qs = MagicMock()
        qs.exists.return_value = False
        filter.return_value = qs
        request = factory.post('/api/approve/request/1')
        request.user = mock_user  
        response = approve_request(request,1)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.requests.Customer.objects.create')
    @patch('hsabackend.views.requests.Job')
    @patch('hsabackend.views.requests.Organization.objects.get')
    @patch('hsabackend.views.requests.Request.objects.filter')
    def test_approve_valid(self,filter, org, job, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        factory = APIRequestFactory()
        qs = MagicMock(name= "req qs")
        qs.exists.return_value = True

        the_req_mock = MagicMock(name = 'the req mock')
        qs.__getitem__.side_effect = lambda x: the_req_mock

        job_mock = MagicMock()
        job.return_value = job_mock
        cust_mock = MagicMock(name="cust mock")
        customer.return_value = cust_mock
        
        filter.return_value = qs
        request = factory.post('/api/approve/request/1')
        request.user = mock_user  
        response = approve_request(request,1)
        assert response.status_code == status.HTTP_200_OK
        the_req_mock.delete.assert_called_once()
        job_mock.save.assert_called_once()
        customer.assert_called_once()
