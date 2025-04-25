from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.views.jobs import get_job_individual_data, get_job_table_data, create_job, edit_job, get_jobs_by_contractor
from rest_framework.test import APITestCase
from hsabackend.models.organization import Organization
from hsabackend.models.customer import Customer
from hsabackend.models.service import Service
from hsabackend.models.material import Material
from hsabackend.models.contractor import Contractor
from hsabackend.models.job_service import JobService
from hsabackend.models.job_material import JobMaterial
from hsabackend.models.job_contractor import JobContractor
from django.db.models import QuerySet
from django.db.models import Q
from unittest.mock import call
from hsabackend.models.job import Job
from django.core.exceptions import ValidationError

class jobViewTest(APITestCase):
    def test_get_job_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = get_job_table_data(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_table_data_invalid(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        get.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs?search')
        request.user = mock_user  
        response = get_job_table_data(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.jobs.Job.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_table_data_valid_query(self,get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        get.return_value = org
        qs = MagicMock(spec=QuerySet)
        filter.return_value = qs
        

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs?search=bob&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_job_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        qs.filter.assert_called_with(Q(customer__first_name__icontains='bob') | Q(customer__last_name__icontains='bob') | Q(start_date__icontains='bob') | Q(end_date__icontains='bob') | Q(job_status__icontains='bob') | Q(description__icontains='bob')) 

    @patch('hsabackend.views.jobs.Job.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_table_data_valid_empty_query(self, get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.pk = 1
        org.is_onboarding = False
        get.return_value = org
        filter.return_value = MagicMock(spec=QuerySet)
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs?search&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_job_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        filter.assert_called_with(organization=1)
    
    def test_get_job_individual_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False

        factory = APIRequestFactory()
        request = factory.get('/api/get/job/1')

        response = get_job_individual_data(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_individual_data_job_not_found(self, org, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        job.return_value = None
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        factory = APIRequestFactory()
        request = factory.get('/api/get/job/1')
        request.user = mock_user  

        response = get_job_individual_data(request, 1)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_individual_data_valid(self, get_org, get_job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org = Organization()
        org.pk = 1
        org.is_onboarding = False
        get_org.return_value = org

        mock_response = {
            "id": 1,
            "jobStatus": "",
            "startDate": "",
            "endDate": "",
            "description": "",
            "customerName": "",
            "customerID": 1,
            "requestorAddress": "",
            "requestorCity": "",
            "requestorState": "",
            "requestorZip": ""
        }

        job = Mock(spec=Job)
        job.pk = 1
        job.json.return_value = mock_response
        get_job.return_value = job

        factory = APIRequestFactory()
        request = factory.get('/api/get/job/1')
        request.user = mock_user  

        response = get_job_individual_data(request, 1)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"] == mock_response

    def test_create_job_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('api/create/job')
        request.user = mock_user  
        response = create_job(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.jobs.Customer.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_create_job_auth_invalid(self, org, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        customer.return_value = Customer()
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        
        factory = APIRequestFactory()
        request = factory.post('api/create/job',
            data={
                "jobStatus": "created",
                "startDate": "2026-01-02",
                "endDate": "2026-02-02",
                "description": "Test Job",
                "customerID": 1,
                "city": "Test City",
                "state": "Iowa",
                "zip": "99999",
                "address": "Test Address",
                "contractors": [
                    { 
                        "id": 2
                    },
                    {
                        "id": 4
                    }
                ],
                "services": [
                    {
                        "id": 2
                    }
                ],
                "materials": [
                    {
                        "id": 2,
                        "unitsUsed": 0,
                        "pricePerUnit": 0.00
                    },
                    {
                        "id": 4,
                        "unitsUsed": 0,
                        "pricePerUnit": 0.00
                    }
                ]
            })
        request.user = mock_user  
        response = create_job(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.jobs.Customer.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.jobs.Service.objects.get')
    @patch('hsabackend.views.jobs.Material.objects.get')
    @patch('hsabackend.views.jobs.Contractor.objects.get')
    @patch('hsabackend.views.jobs.Job')
    @patch('hsabackend.views.jobs.JobService')
    @patch('hsabackend.views.jobs.JobMaterial')
    @patch('hsabackend.views.jobs.JobContractor')
    def test_calls_save_if_valid(self, job_contractor, job_material, job_service, job_name, contractor, material, service, org, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        customer.return_value = Customer()
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        service.return_value = Service()
        material.return_value = Material()
        contractor.return_value = Contractor()

        job_name_obj = MagicMock(spec=Job)
        job_name.return_value = job_name_obj

        job_service_obj = MagicMock(spec=JobService)
        job_service.return_value = job_service_obj

        job_material_obj = MagicMock(spec=JobMaterial)
        job_material.return_value = job_material_obj

        job_contractor_obj = MagicMock(spec=JobContractor)
        job_contractor.return_value = job_contractor_obj
        
        factory = APIRequestFactory()

        mock_data = {
                "jobStatus": "created",
                "startDate": "2026-01-02",
                "endDate": "2026-02-02",
                "description": "Test Job",
                "customerID": 1,
                "city": "Test City",
                "state": "Iowa",
                "zip": "99999",
                "address": "Test Address",
                "contractors": [
                    { 
                        "id": 2
                    },
                    {
                        "id": 4
                    }
                ],
                "services": [
                    {
                        "id": 2
                    }
                ],
                "materials": [
                    {
                        "id": 2,
                        "unitsUsed": 0,
                        "pricePerUnit": 0.00
                    },
                    {
                        "id": 4,
                        "unitsUsed": 0,
                        "pricePerUnit": 0.00
                    }
                ]
            }

        request = factory.post('api/create/job', data=mock_data, format='json')
        request.user = mock_user   
        response = create_job(request)

        job_name_obj.save.assert_called_once()

        assert job_service_obj.save.call_count == len(mock_data["services"])
        assert job_material_obj.save.call_count == len(mock_data["materials"])
        assert job_contractor_obj.save.call_count == len(mock_data["contractors"])

        assert response.status_code == status.HTTP_201_CREATED

#     def test_edit_job_unauth(self):
#         mock_user = Mock(spec=User)
#         mock_user.is_authenticated = False
        
#         factory = APIRequestFactory()
#         request = factory.post('/api/edit/job/1')
#         request.user = mock_user  
#         response = edit_job(request, 1)
        
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     @patch('hsabackend.views.jobs.Job.objects.get')
#     @patch('hsabackend.views.jobs.Organization.objects.get')
#     def test_edit_job_not_found(self,org, job_name):
#         mock_user = Mock(spec=User)
#         mock_user.is_authenticated = True
#         job_name.return_value = None
#         organization = Organization()
#         organization.is_onboarding = False
#         org.return_value = organization
        
#         factory = APIRequestFactory()
#         request = factory.post('/api/edit/job/0')
#         request.user = mock_user  
#         response = edit_job(request, 1)

#         assert response.status_code == status.HTTP_404_NOT_FOUND

#     @patch('hsabackend.views.jobs.Customer.objects.get')
#     @patch('hsabackend.views.jobs.Job.objects.get')
#     @patch('hsabackend.views.jobs.Organization.objects.get')
#     def test_edit_job_invalid(self, org, job_name, customer):
#         mock_user = Mock(spec=User)
#         mock_user.is_authenticated = True
#         mock_job_name = MagicMock(spec=Job)
#         customer.return_value = Customer()
#         job_name.return_value = mock_job_name
#         organization = Organization()
#         organization.is_onboarding = False
#         org.return_value = organization
        
#         mock_job_name.full_clean.side_effect = ValidationError({'description': ['This field is required.']})

#         factory = APIRequestFactory()
#         request = factory.post('/api/edit/job/1',
#             data={
#                 "job_status": "created",
#                 "start_date": "2026-01-02",
#                 "end_date": "2026-02-02",
#                 "description": "Test Job",
#                 "city": "Test City",
#                 "state": "Iowa",
#                 "zip": "99999",
#                 "address": "Test Address",
#             })
#         request.user = mock_user  
#         response = edit_job(request, 1)
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST

#     @patch('hsabackend.views.jobs.Customer.objects.get')
#     @patch('hsabackend.views.jobs.Job.objects.get')
#     @patch('hsabackend.views.jobs.Organization.objects.get')
#     def test_edit_job_valid(self, org, job_name, customer):
#         mock_user = Mock(spec=User)
#         mock_user.is_authenticated = True
#         mock_job_name = MagicMock(spec=Job)
#         customer.return_value = Customer()
#         job_name.return_value = mock_job_name
#         organization = Organization()
#         organization.is_onboarding = False
#         org.return_value = organization

#         factory = APIRequestFactory()
#         request = factory.post('/api/edit/job/1',
#             data={
#                 "job_status": "created",
#                 "start_date": "2026-01-02",
#                 "end_date": "2026-02-02",
#                 "description": "Test Job",
#                 "city": "Test City",
#                 "state": "Iowa",
#                 "zip": "99999",
#                 "address": "Test Address",
#             })
#         request.user = mock_user  
#         response = edit_job(request, 1)
        
#         assert response.status_code == status.HTTP_200_OK

# class JobsByCustomer(APITestCase):
    
#     @patch('hsabackend.views.jobs.Organization.objects.get')
#     def test_no_pagesize(self, orgg):
#         mock_user = Mock(spec=User)
#         mock_user.is_authenticated = True
        
#         org = Organization()
#         org.is_onboarding = False
#         orgg.return_value = org
#         factory = APIRequestFactory()
#         request = factory.get('/api/get/jobs/by-contractor?offset=2')
#         request.user = mock_user  
#         response = get_jobs_by_contractor(request, 1)
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
    
#     def test_get_job_by_contractor_invalid_contractor(self):
#         pass

#     def test_fetch_ok(self):
#         pass