from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.views.jobs_contractors import delete_cached_job_contractor, get_job_contractor_table_data, create_job_contractor, delete_job_contractor
from rest_framework.test import APITestCase
from hsabackend.models.organization import Organization
from django.db.models import QuerySet
from hsabackend.models.contractor import Contractor
from hsabackend.models.job import Job
from hsabackend.models.job_contractor import JobContractor
from django.core.exceptions import ValidationError

class contractorViewTest(APITestCase):
    def test_get_job_contractor_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/job/1/contractors?pagesize=100&offset=0')
        request.user = mock_user  
        response = get_job_contractor_table_data(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @patch('hsabackend.views.jobs_contractors.Job.objects.get')
    @patch('hsabackend.views.jobs_contractors.Contractor.objects.get')
    @patch('hsabackend.views.jobs_contractors.Organization.objects.get')
    def test_get_job_contractor_table_data_invalid(self, org, contractor, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job.return_value = Job()
        contractor.return_value = Contractor()
        org.return_value = Organization()
        factory = APIRequestFactory()
        request = factory.get('/api/get/job/1/contractors?pagesize')
        request.user = mock_user  
        response = get_job_contractor_table_data(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.jobs_contractors.Contractor.objects.get')
    @patch('hsabackend.views.jobs_contractors.Organization.objects.get')
    def test_get_job_contractor_table_job_not_found(self, org, contractor):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        contractor.return_value = Contractor()
        org.return_value = Organization()

        factory = APIRequestFactory()
        request = factory.get('/api/get/job/1/contractors?pagesize=100&offset=10')
        request.user = mock_user  
        response = get_job_contractor_table_data(request, 1)
        assert response.status_code == status.HTTP_404_NOT_FOUND


    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.views.jobs.Organization.objects.get')
    def test_get_job_table_data_valid_empty_query(self, org, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job.return_value = Job()
        org.return_value = Organization()
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/job/1/contractors?pagesize=10&offset=10')
        request.user = mock_user  
        response = get_job_contractor_table_data(request, 1)
        
        assert response.status_code == status.HTTP_200_OK

    def test_job_create_contractor_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('api/create/job/1/contractor')
        request.user = mock_user  
        response = create_job_contractor(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.jobs_contractors.JobContractor.objects.filter')
    @patch('hsabackend.views.jobs_contractors.Contractor.objects.get')
    @patch('hsabackend.views.jobs_contractors.Job.objects.get')
    @patch('hsabackend.views.jobs_contractors.Organization.objects.get')
    def test_job_create_contractor_auth_invalid(self, org, job, contractor, job_contractor_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_contractor_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = True

        contractor.return_value = Contractor()
        job.return_value = Job()
        org.return_value = Organization()

        mockdata = {
            "contractors": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ]
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/job/1/contractor', data=mockdata, format='json')
        request.user = mock_user  
        response = create_job_contractor(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.jobs_contractors.JobContractor.objects.filter')
    @patch('hsabackend.views.jobs_contractors.Contractor.objects.get')
    @patch('hsabackend.views.jobs_contractors.Job.objects.get')
    @patch('hsabackend.views.jobs_contractors.Organization.objects.get')
    def test_job_create_contractor_request_empty(self, org, job, contractor, job_contractor_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_contractor_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = True

        contractor.return_value = Contractor()
        job.return_value = Job()
        org.return_value = Organization()

        mockdata = {
            "contractors": []
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/job/1/contractor', data=mockdata, format='json')
        request.user = mock_user  
        response = create_job_contractor(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.jobs_contractors.JobContractor.objects.filter')
    @patch('hsabackend.views.jobs_contractors.Job.objects.get')
    @patch('hsabackend.views.jobs_contractors.Organization.objects.get')
    @patch('hsabackend.views.jobs_contractors.Contractor.objects.get')
    @patch('hsabackend.views.jobs_contractors.JobContractor')
    def test_job_create_contractor_entry_already_exist(self, job_contractor, contractor, org, job, job_contractor_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_contractor_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = True

        job.return_value = Job()
        org.return_value = Organization()
        contractor.return_value = Contractor()
        job_contractor_obj = MagicMock(spec=JobContractor)
        job_contractor.return_value = job_contractor_obj

        mockdata = {
            "contractors": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ]
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/job/1/contractor', data=mockdata, format='json')
        request.user = mock_user

        response = create_job_contractor(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.jobs_contractors.JobContractor.objects.filter')
    @patch('hsabackend.views.jobs_contractors.Job.objects.get')
    @patch('hsabackend.views.jobs_contractors.Organization.objects.get')
    @patch('hsabackend.views.jobs_contractors.Contractor.objects.get')
    @patch('hsabackend.views.jobs_contractors.JobContractor')
    def test_calls_save_if_valid(self, job_contractor, contractor, org, job, job_contractor_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_contractor_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = False

        job.return_value = Job()
        org.return_value = Organization()
        contractor.return_value = Contractor()
        job_contractor_obj = MagicMock(spec=JobContractor)
        job_contractor.return_value = job_contractor_obj

        mockdata = {
            "contractors": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ]
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/job/1/contractor', data=mockdata, format='json')
        request.user = mock_user

        response = create_job_contractor(request, 1)
        job_contractor_obj.save.call_count == len(mockdata["contractors"])
        assert response.status_code == status.HTTP_201_CREATED

    def test_job_delete_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/job/1/contractor/1')
        request.user = mock_user  
        response = delete_job_contractor(request, 1, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.jobs_contractors.JobContractor.objects.filter')
    @patch('hsabackend.views.jobs_contractors.Organization.objects.get')
    def test_job_delete_not_found(self, org, job_contractor_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_contractor_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = False 
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/job/1/contractor/1')
        request.user = mock_user  
        response = delete_job_contractor(request, 1, 1)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.jobs_contractors.JobContractor.objects.filter')
    @patch('hsabackend.views.jobs_contractors.Organization.objects.get')
    def test_delete_valid(self, org, job_contractor_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_contractor_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = True 
        contractor_mock = MagicMock()
        job_serivce_qs.__getitem__.side_effect = lambda x: contractor_mock
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/job/1/contractor/1')
        request.user = mock_user  
        response = delete_job_contractor(request, 1, 1)
        
        assert response.status_code == status.HTTP_200_OK
        contractor_mock.delete.assert_called_once

    @patch('hsabackend.utils.auth_wrapper.Organization')
    def test_delete_cached_invalid(self,auth_org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mockdata = {
            "jobContractors": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ],
        }
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/job/1/contractors', data=mockdata, format='json')
        request.user = mock_user  
        response = delete_cached_job_contractor(request, 1)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.jobs_contractors.JobContractor.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization')
    def test_delete_cached_valid(self, auth_org, job_contractor):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        job_contractor_obj = MagicMock(spec=JobContractor)
        job_contractor.return_value = job_contractor_obj

        mockdata = {
            "jobContractors": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ],
        }
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/job/1/contractors', data=mockdata, format='json')
        request.user = mock_user  
        response = delete_cached_job_contractor(request, 1)
        
        assert response.status_code == status.HTTP_200_OK
        assert job_contractor_obj.delete.call_count == len(mockdata["jobContractors"])
