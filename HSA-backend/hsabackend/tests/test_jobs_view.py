from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.views.jobs import get_job_individual_data, get_job_table_data, create_job, edit_job, get_jobs_by_contractor, get_job_excluded_table_data, delete_job, get_invoicable_jobs, get_invoicable_jobs_per_invoice
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

    
class JobsByCustomer(APITestCase):
    
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_no_pagesize(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/by-contractor?offset=2&contractor=2')
        request.user = mock_user  
        response = get_jobs_by_contractor(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_by_contractor_invalid_contractor(self,orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/by-contractor?offset=2&pagesize=10&contractor=ajajaj')
        request.user = mock_user  
        response = get_jobs_by_contractor(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_fetch_ok(self,orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/by-contractor?offset=2&contractor=2&pagesize=10')
        request.user = mock_user  
        response = get_jobs_by_contractor(request)
        assert response.status_code == status.HTTP_200_OK

class JobExcludedTableData(APITestCase):
    
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def job_excluded_no_pagesize(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/exclude?offset=10')
        request.user = mock_user  
        response = get_job_excluded_table_data(request)

        assert response.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def job_excluded_invalid_pagesize(self,orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/exclude?offset=10&pagesize=sss')
        request.user = mock_user  
        response = get_job_excluded_table_data(request)

        assert response.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def job_excluded_ok(self,orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/exclude?offset=10&pagesize=10')
        request.user = mock_user  
        response = get_job_excluded_table_data(request)

        assert response.status_code == 200

class TestGetJobTable(APITestCase):
        
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

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_table_data_nonint(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        get.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs?pagesize=1&offset=c')
        request.user = mock_user  
        response = get_job_table_data(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_table_bad_stat(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        get.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs?pagesize=1&offset=2&status=sss')
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
        request = factory.get('/api/get/jobs?search=bob&pagesize=10&offset=10&status=completed')
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
        request = factory.get('/api/get/jobs?search&pagesize=10&offset=10&status=completed')
        request.user = mock_user  
        response = get_job_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        filter.assert_called_with(organization=1, job_status='completed')

class CreateJobTest(APITestCase):
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

    
    @patch('hsabackend.views.jobs.Customer.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.jobs.Service.objects.get')
    @patch('hsabackend.views.jobs.Material.objects.get')
    @patch('hsabackend.views.jobs.Contractor.objects.get')
    @patch('hsabackend.views.jobs.Job')
    @patch('hsabackend.views.jobs.JobService')
    @patch('hsabackend.views.jobs.JobMaterial')
    @patch('hsabackend.views.jobs.JobContractor')
    def test_validation_error(self, job_contractor, job_material, job_service, job_name, contractor, material, service, org, customer):
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
        job_name_obj.full_clean.side_effect = ValidationError({'name': ['This field is required.']})
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

        assert response.status_code == 400

class GetJobExcludedTest(APITestCase):
    
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_no_pagesize(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        factory = APIRequestFactory()
        request = factory.get('api/get/jobs/exclude?offset=1')
        request.user = mock_user   

        res = get_job_excluded_table_data(request)

        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_bad_pagesize(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        factory = APIRequestFactory()
        request = factory.get('api/get/jobs/exclude?offset=1&pagesize=s')
        request.user = mock_user   

        res = get_job_excluded_table_data(request)

        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.jobs.Job.objects.filter')
    def test_ok(self, filter, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        mock_filter = Mock(name="qs")
        filter.return_value = mock_filter
        exclude = Mock(name = "exclude")
        mock_filter.exclude.return_value = exclude
        filter2 = MagicMock(name = "filter2")
        exclude.filter.return_value = filter2


        factory = APIRequestFactory()
        request = factory.get('api/get/jobs/exclude?offset=1&pagesize=2')
        request.user = mock_user   

        res = get_job_excluded_table_data(request)

        assert res.status_code == 200

class TestEditJobs(APITestCase):
    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_job_not_found(self,org, job_name):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_name.side_effect = Job.DoesNotExist
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/job/0')
        request.user = mock_user  
        response = edit_job(request, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.jobs.Customer.objects.get')
    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_job_invalid(self, org, job_name, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_job_name = MagicMock(spec=Job)
        customer.return_value = Customer()
        job_name.return_value = mock_job_name
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        
        mock_job_name.full_clean.side_effect = ValidationError({'description': ['This field is required.']})

        factory = APIRequestFactory()
        request = factory.post('/api/edit/job/1',
            data={
                "job_status": "created",
                "start_date": "2026-01-02",
                "end_date": "2026-02-02",
                "description": "Test Job",
                "city": "Test City",
                "state": "Iowa",
                "zip": "99999",
                "address": "Test Address",
            })
        request.user = mock_user  
        response = edit_job(request, 1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.jobs.Customer.objects.get')
    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_job_is_completed(self, org, job_name, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_job_name = MagicMock(spec=Job)
        mock_job_name.job_status = "completed"
        customer.return_value = Customer()
        job_name.return_value = mock_job_name
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        factory = APIRequestFactory()
        request = factory.post('/api/edit/job/1',
            data={
                "job_status": "created",
                "start_date": "2026-01-02",
                "end_date": "2026-02-02",
                "description": "Test Job",
                "city": "Test City",
                "state": "Iowa",
                "zip": "99999",
                "address": "Test Address",
            })
        request.user = mock_user  
        response = edit_job(request, 1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    @patch('hsabackend.views.jobs.Customer.objects.get')
    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_job_valid(self, org, job_name, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_job_name = MagicMock(spec=Job)
        customer.return_value = Customer()
        job_name.return_value = mock_job_name
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        factory = APIRequestFactory()
        request = factory.post('/api/edit/job/1',
            data={
                "job_status": "created",
                "start_date": "2026-01-02",
                "end_date": "2026-02-02",
                "description": "Test Job",
                "city": "Test City",
                "state": "Iowa",
                "zip": "99999",
                "address": "Test Address",
            })
        request.user = mock_user  
        response = edit_job(request, 1)
        
        assert response.status_code == status.HTTP_200_OK


class TestDeleteJobs(APITestCase):
    @patch('hsabackend.views.jobs.Job.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_delete_job_not_found(self, org, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        mock_job = Mock()
        mock_job.exists.return_value = False
        job.return_value = mock_job

        factory = APIRequestFactory()
        request = factory.post('/api/delete/job/1')
        request.user = mock_user

        res = delete_job(request, 1)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.jobs.Job.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_delete_job_completed(self, org, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        mock_job = MagicMock()
        mock_job.exists.return_value = True
        job.return_value = mock_job

        mock_job_obj = MagicMock(name="Job")
        mock_job_obj.job_status = "completed"  
        mock_job.__getitem__.side_effect = lambda x: mock_job_obj

        factory = APIRequestFactory()
        request = factory.post('/api/delete/job/1')
        request.user = mock_user

        res = delete_job(request, 1)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.jobs.Job.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_delete_job_ok(self, org, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        mock_job = MagicMock()
        mock_job.exists.return_value = True
        job.return_value = mock_job

        mock_job_obj = MagicMock(name="Job")
        mock_job.__getitem__.side_effect = lambda x: mock_job_obj

        factory = APIRequestFactory()
        request = factory.post('/api/delete/job/1')
        request.user = mock_user

        res = delete_job(request, 1)
        mock_job_obj.delete.assert_called_once()
        assert res.status_code == status.HTTP_200_OK

class TestGetInvoicableJobs(APITestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_missing_params(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization 

        factory = APIRequestFactory()
        request = factory.get('api/get/invoicable/jobs?pagesize=10')
        request.user = mock_user

        res = get_invoicable_jobs(request)
        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_invalid_params(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization 

        factory = APIRequestFactory()
        request = factory.get('api/get/invoicable/jobs?pagesize=10&customer=s')
        request.user = mock_user

        res = get_invoicable_jobs(request)
        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.jobs.Job.objects.filter')
    def test_ok(self,filter, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization 

        factory = APIRequestFactory()
        request = factory.get('api/get/invoicable/jobs?pagesize=10&customer=1')
        request.user = mock_user

        filter.return_value = MagicMock()

        res = get_invoicable_jobs(request)
        assert res.status_code == 200

class TestInvoicableJobsPerInvoice(APITestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_no_parameters(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization 

        factory = APIRequestFactory()
        request = factory.get('api/get/jobs/for-invoice?&invoice=1')
        request.user = mock_user

        res = get_invoicable_jobs_per_invoice(request)
        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_bad_parameters(self, org,):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization 

        factory = APIRequestFactory()
        request = factory.get('api/get/jobs/for-invoice?pagesize=a&invoice=1')
        request.user = mock_user

        res = get_invoicable_jobs_per_invoice(request)
        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.jobs.Job.objects.filter')
    @patch('hsabackend.views.jobs.Invoice.objects.filter')
    def test_invoice_not_exists(self, inv,filter , org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization 

        factory = APIRequestFactory()
        request = factory.get('api/get/jobs/for-invoice?pagesize=4&invoice=1')
        request.user = mock_user
        
        mock_qs = MagicMock()
        inv.return_value = mock_qs

        mock_qs.exists.return_value = False

        res = get_invoicable_jobs_per_invoice(request)
        assert res.status_code == 404

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.jobs.Job.objects.filter')
    @patch('hsabackend.views.jobs.Invoice.objects.filter')
    def test_ok(self, inv,filter , org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization 

        factory = APIRequestFactory()
        request = factory.get('api/get/jobs/for-invoice?pagesize=4&invoice=1')
        request.user = mock_user
        
        mock_qs = MagicMock()
        inv.return_value = mock_qs


        res = get_invoicable_jobs_per_invoice(request)
        assert res.status_code == 200