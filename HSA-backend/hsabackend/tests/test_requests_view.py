from rest_framework.test import APITestCase
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status
from hsabackend.views.requests import delete_request, approve_request, create_request, get_individual_request_data, get_filtered_request_data
from hsabackend.models.organization import Organization
from hsabackend.models.request import Request
from hsabackend.models.customer import Customer
from hsabackend.models.job import Job
from django.db.models import QuerySet
from django.db.models import Q

class RequestView(APITestCase):

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

    @patch('hsabackend.views.requests.Organization.objects.get')
    @patch('hsabackend.views.requests.Request.objects.get')
    @patch('hsabackend.views.requests.Customer')
    @patch('hsabackend.views.requests.Job')
    def test_approve_valid(self, job, customer, get, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization(
            org_name = "Test Org",
            org_email = "test@test.com",
            org_city = "test city",
            org_requestor_state = "IA",
            org_requestor_zip = "99999",
            org_requestor_address = "Test address",
            org_phone = "124567890",
            org_owner_first_name = "Test",
            org_owner_last_name = "Test",
            is_onboarding = False,
        )
        org.return_value = organization

        req = MagicMock(spec=Request)
        req.requester_first_name = "Test"
        req.requester_last_name = "Test"
        req.requester_email = "test@gmail.com"
        req.requester_phone = "1234567890"
        req.organization = organization
        get.return_value = req
        get

        customer_mock = MagicMock(spec=Customer)
        customer_mock.first_name = "Test"
        customer_mock.last_name = "Test"
        customer_mock.email = "test@gmail.com"
        customer_mock.phone_no = "1234567890"
        customer_mock.notes = ""
        customer_mock.organization = organization
        customer.return_value = customer_mock

        job_mock = MagicMock(spec=Job)
        job_mock.requestor_city = req.requester_city
        job_mock.requestor_state = req.requester_state
        job_mock.requestor_zip = req.requester_zip
        job_mock.requestor_address = req.requester_address
        job_mock.description = ""
        job_mock.customer = customer_mock
        job_mock.organization = organization
        job.return_value = job_mock
        
        factory = APIRequestFactory()
        
        request = factory.post('/api/approve/request/1')
        request.user = mock_user  
        request.org = organization

        response = approve_request(request,1)

        assert response.status_code == status.HTTP_200_OK

class TestIndividualRequest(APITestCase):

    @patch('hsabackend.views.requests.Request.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_not_found(self, org, req):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        req.side_effect = Request.DoesNotExist

        factory = APIRequestFactory()
        request = factory.get('api/get/request/1')
        request.user = mock_user  
        request.org = organization

        res = get_individual_request_data(request, 1)
        assert res.status_code == 404
    
    @patch('hsabackend.views.requests.Request.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_ok(self, org, req):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        factory = APIRequestFactory()
        request = factory.get('api/get/request/1')
        request.user = mock_user  
        request.org = organization

        res = get_individual_request_data(request, 1)
        assert res.status_code == 200

class TestGetFiltered(APITestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_bad_param(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        factory = APIRequestFactory()
        request = factory.get('api/get/requests/filter')
        request.user = mock_user  
        request.org = organization

        res = get_filtered_request_data(request)
        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.requests.Request.objects.filter')
    def test_ok(self, filter, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        factory = APIRequestFactory()
        request = factory.get('api/get/requests/filter?status=approved&pagesize=10&offset=10')
        request.user = mock_user  
        request.org = organization

        mock_req = MagicMock()
        filter1 = MagicMock()
        filter.return_value = filter1
        filter1.return_value = [mock_req]

        res = get_filtered_request_data(request)
        assert res.status_code == 200