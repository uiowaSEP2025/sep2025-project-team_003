from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.views.job_templates_services import delete_cached_job_template_service, get_job_template_service_table_data, create_job_template_service, delete_job_template_service
from rest_framework.test import APITestCase
from hsabackend.models.organization import Organization
from django.db.models import QuerySet
from django.db.models import Q
from hsabackend.models.service import Service
from hsabackend.models.job_template import JobTemplate
from django.core.exceptions import ValidationError

class ServiceViewTest(APITestCase):
    def test_get_job_template_service_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplate/1/services?pagesize=100&offset=0')
        request.user = mock_user  
        response = get_job_template_service_table_data(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @patch('hsabackend.views.job_templates_services.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_services.Service.objects.get')
    @patch('hsabackend.views.job_templates_services.Organization.objects.get')
    def test_get_job_template_service_table_data_invalid(self, org, service, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job.return_value = JobTemplate()
        service.return_value = Service()
        org.return_value = Organization()
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplate/1/services?pagesize')
        request.user = mock_user  
        response = get_job_template_service_table_data(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.job_templates_services.Service.objects.get')
    @patch('hsabackend.views.job_templates_services.Organization.objects.get')
    def test_get_job_template_service_table_job_template_not_found(self, org, service):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        service.return_value = Service()
        org.return_value = Organization()

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplate/1/services?pagesize=100&offset=10')
        request.user = mock_user  
        response = get_job_template_service_table_data(request, 1)
        assert response.status_code == status.HTTP_404_NOT_FOUND


    @patch('hsabackend.views.job_templates_services.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_services.Organization.objects.get')
    def test_get_job_template_table_data_valid_empty_query(self, org, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job.return_value = JobTemplate()
        org.return_value = Organization()
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplate/1/services?pagesize=10&offset=10')
        request.user = mock_user  
        response = get_job_template_service_table_data(request, 1)
        
        assert response.status_code == status.HTTP_200_OK

    def test_job_template_create_service_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate/1/service')
        request.user = mock_user  
        response = create_job_template_service(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.job_templates_services.JobTemplateService.objects.filter')
    @patch('hsabackend.views.job_templates_services.Service.objects.get')
    @patch('hsabackend.views.job_templates_services.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_services.Organization.objects.get')
    def test_job_template_create_service_auth_invalid(self, org, job, service, job_service_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_service_qs = MagicMock(spec=QuerySet)
        job_service_filter.return_value = job_service_qs
        job_service_qs.exists.return_value = True

        service.return_value = Service()
        job.return_value = JobTemplate()
        org.return_value = Organization()

        mockdata = {
            "services": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ]
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate/1/service', data=mockdata, format='json')
        request.user = mock_user  
        response = create_job_template_service(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    @patch('hsabackend.views.job_templates_services.JobTemplateService.objects.filter')
    @patch('hsabackend.views.job_templates_services.Service.objects.get')
    @patch('hsabackend.views.job_templates_services.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_services.Organization.objects.get')
    def test_job_template_create_service_request_empty(self, org, job, service, job_service_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_service_qs = MagicMock(spec=QuerySet)
        job_service_filter.return_value = job_service_qs
        job_service_qs.exists.return_value = True

        service.return_value = Service()
        job.return_value = JobTemplate()
        org.return_value = Organization()

        mockdata = {
            "services": []
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate/1/service', data=mockdata, format='json')
        request.user = mock_user  
        response = create_job_template_service(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    @patch('hsabackend.views.job_templates_services.JobTemplateService.objects.filter')
    @patch('hsabackend.views.job_templates_services.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_services.Organization.objects.get')
    @patch('hsabackend.views.job_templates_services.Service.objects.get')
    @patch('hsabackend.views.job_templates_services.JobTemplateService')
    def test_job_template_create_service_entry_already_exist(self, job_service, service, org, job, job_service_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_service_qs = MagicMock(spec=QuerySet)
        job_service_filter.return_value = job_service_qs
        job_service_qs.exists.return_value = True

        job.return_value = JobTemplate()
        org.return_value = Organization()
        service.return_value = Service()
        job_service_obj = MagicMock(spec=JobTemplateService)
        job_service.return_value = job_service_obj

        mockdata = {
            "services": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ]
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate/1/service', data=mockdata, format='json')
        request.user = mock_user

        response = create_job_template_service(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.job_templates_services.JobTemplateService.objects.filter')
    @patch('hsabackend.views.job_templates_services.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_services.Organization.objects.get')
    @patch('hsabackend.views.job_templates_services.Service.objects.get')
    @patch('hsabackend.views.job_templates_services.JobTemplateService')
    def test_calls_save_if_valid(self, job_service, service, org, job, job_service_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_service_qs = MagicMock(spec=QuerySet)
        job_service_filter.return_value = job_service_qs
        job_service_qs.exists.return_value = False

        job.return_value = JobTemplate()
        org.return_value = Organization()
        service.return_value = Service()
        job_service_obj = MagicMock(spec=JobTemplateService)
        job_service.return_value = job_service_obj

        mockdata = {
            "services": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ]
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate/1/service', data=mockdata, format='json')
        request.user = mock_user

        response = create_job_template_service(request, 1)
        assert job_service_obj.save.call_count == len(mockdata["services"])
        assert response.status_code == status.HTTP_201_CREATED

    def test_job_template_delete_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/jobtemplate/1/service/1')
        request.user = mock_user  
        response = delete_job_template_service(request, 1, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.job_templates_services.JobTemplateService.objects.filter')
    @patch('hsabackend.views.job_templates_services.Organization.objects.get')
    def test_job_template_delete_not_found(self, org, job_service_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        job_service_qs = MagicMock(spec=QuerySet)
        job_service_filter.return_value = job_service_qs
        job_service_qs.exists.return_value = False 
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/jobtemplate/1/service/1')
        request.user = mock_user  
        response = delete_job_template_service(request, 1, 1)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.job_templates_services.JobTemplateService.objects.filter')
    @patch('hsabackend.views.job_templates_services.Organization.objects.get')
    def test_delete_valid(self, org, job_service_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        job_service_qs = MagicMock(spec=QuerySet)
        job_service_filter.return_value = job_service_qs
        job_service_qs.exists.return_value = True 
        service_mock = MagicMock()
        job_service_qs.__getitem__.side_effect = lambda x: service_mock
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/jobtemplate/1/service/1')
        request.user = mock_user  
        response = delete_job_template_service(request, 1, 1)
        
        assert response.status_code == status.HTTP_200_OK
        service_mock.delete.assert_called_once

    @patch('hsabackend.utils.auth_wrapper.Organization')
    def test_delete_cached_invalid(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mockdata = {
            "jobTemplateServices": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ],
        }
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/jobtemplate/1/services', data=mockdata, format='json')
        request.user = mock_user  
        response = delete_cached_job_template_service(request, 1)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.job_templates_services.JobTemplateService.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization')
    def test_delete_cached_valid(self, org, job_service):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        job_service_obj = MagicMock(spec=JobTemplateService)
        job_service.return_value = job_service_obj

        mockdata = {
            "jobTemplateServices": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ],
        }
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/jobtemplate/1/services', data=mockdata, format='json')
        request.user = mock_user  
        response = delete_cached_job_template_service(request, 1)
        
        assert response.status_code == status.HTTP_200_OK
        assert job_service_obj.delete.call_count == len(mockdata["jobTemplateServices"])
