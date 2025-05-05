from rest_framework.test import APITestCase
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status

from hsabackend.tests import BaseTestCase
from hsabackend.views.requests import get_org_request_data, delete_request, approve_request, create_request
from hsabackend.models.organization import Organization
from hsabackend.models.request import Request
from hsabackend.models.customer import Customer
from hsabackend.models.job import Job
from django.db.models import QuerySet
from django.db.models import Q

class RequestView(BaseTestCase):
    def test_get_customer_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/requests?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = get_org_request_data(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.requests.Organization.objects.get')
    def test_create_request_org_not_found(self, mock_get):
        mock_get.side_effect = Organization.DoesNotExist

        factory = APIRequestFactory()
        req = factory.post('/api/request/create/999', {}, format='json')
        resp = create_request(req, 999)

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.data['message'] == "Organization 999 not found"

    @patch('hsabackend.views.requests.Request')
    @patch('hsabackend.views.requests.Organization.objects.get')
    def test_create_request_success(self, mock_get_org, mock_request_cls):
        """
        Given valid payload and existing Organization, the view should:
        - instantiate Request(...)
        - call full_clean()
        - call save()
        - return HTTP 201 with the new request's ID and JSON data
        """
        org = Organization(pk=1)
        mock_get_org.return_value = org

        mock_req = mock_request_cls.return_value
        mock_req.id = 42
        mock_req.json.return_value = {
            "requester_first_name": "Alice",
            "requester_last_name":  "Smith",
            "requester_email":      "alice@example.com",
            "requester_city":       "Springfield",
            "requester_state":      "IL",
            "requester_zip":        "62704",
            "requester_address":    "123 Main St",
            "requester_phone":      "5551234",
            "description":          "Need service",
            "availability":         "Mondays",
            "organization":         1
        }

        payload = {
            "requester_first_name": "Alice",
            "requester_last_name":  "Smith",
            "requester_email":      "alice@example.com",
            "requester_city":       "Springfield",
            "requester_state":      "IL",
            "requester_zip":        "62704",
            "requester_address":    "123 Main St",
            "requester_phone":      "555-1234",
            "description":          "Need service",
            "availability":         "Mondays"
        }

        factory = APIRequestFactory()
        request = factory.post('/api/request/create/1', payload, format='json')

        response = create_request(request, 1)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == "Request created successfully"
        assert response.data['id'] == 42
        assert response.data['data'] == mock_req.json()

        mock_req.full_clean.assert_called_once()
        mock_req.save.assert_called_once()

    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_get_request_table_data_invalid(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        get.return_value = org
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
        
        org = Organization()
        org.is_onboarding = False
        get.return_value = org
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
        org = Organization()
        org.pk = 1
        org.is_onboarding = False
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
        org = Organization()
        org.pk = 1
        org.is_onboarding = False
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
        org = Organization()
        org.pk = 1
        org.is_onboarding = False
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
    @patch('hsabackend.views.requests.Request.objects.get')
    def test_approve_not_exists(self,filter, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        factory = APIRequestFactory()
        qs = MagicMock()
        qs.exists.return_value = False
        filter.return_value = qs
        request = factory.post('/api/approve/request/1')
        request.user = mock_user  
        response = approve_request(request,1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # @patch('hsabackend.views.requests.Organization.objects.get')
    # @patch('hsabackend.views.requests.Request.objects.get')
    # @patch('hsabackend.views.requests.Customer.objects.create')
    # @patch('hsabackend.views.requests.Job.objects.create')
    # def test_approve_valid(self, job, customer, get, org):
    #     mock_user = Mock(spec=User)
    #     mock_user.is_authenticated = True

    #     organization = Organization(
    #         org_name = "Test Org",
    #         org_email = "test@test.com",
    #         org_city = "test city",
    #         org_requestor_state = "IA",
    #         org_requestor_zip = "99999",
    #         org_requestor_address = "Test address",
    #         org_phone = "124567890",
    #         org_owner_first_name = "Test",
    #         org_owner_last_name = "Test",
    #         is_onboarding = False,
    #     )
    #     org.return_value = organization

    #     req = MagicMock(spec=Request)
    #     req.requestor_first_name = "Test"
    #     req.requestor_last_name = "Test"
    #     req.requestor_email = "test@gmail.com"
    #     req.requestor_phone_no = "1234567890"
    #     req.organization = organization
    #     get.return_value = req

    #     customer_mock = MagicMock(spec=Customer)
    #     customer_mock.first_name = "Test"
    #     customer_mock.last_name = "Test"
    #     customer_mock.email = "test@gmail.com"
    #     customer_mock.phone_no = "1234567890"
    #     customer_mock.notes = ""
    #     customer_mock.organization = organization
    #     customer.return_value = customer_mock

    #     job_mock = MagicMock(spec=Job)
    #     job_mock.requestor_city = req.requestor_city
    #     job_mock.requestor_state = req.requestor_state
    #     job_mock.requestor_zip = req.requestor_zip
    #     job_mock.requestor_address = req.requestor_address
    #     job_mock.description = ""
    #     job_mock.customer = customer_mock
    #     job_mock.organization = organization
    #     job.return_value = job_mock
        
    #     factory = APIRequestFactory()
        
    #     request = factory.post('/api/approve/request/1')
    #     request.user = mock_user  
    #     request.org = organization

    #     response = approve_request(request,1)

    #     print(response.status_code, response.data)
    #     assert response.status_code == status.HTTP_200_OK
