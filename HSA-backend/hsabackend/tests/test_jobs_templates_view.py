from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.views.job_templates import get_job_template_table_data, get_job_template_individual_data, create_job_template, edit_job_template
from rest_framework.test import APITestCase
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.models.material import Material
from django.db.models import QuerySet
from django.db.models import Q
from unittest.mock import call
from hsabackend.models.job_template import JobTemplate
from django.core.exceptions import ValidationError

class jobViewTest(APITestCase):
    def test_get_job_template_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplates?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = get_job_template_table_data(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    @patch('hsabackend.views.job_templates.Organization.objects.get')
    def test_get_job_template_table_data_invalid(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplates?search')
        request.user = mock_user  
        response = get_job_template_table_data(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.job_templates.JobTemplate.objects.filter')
    @patch('hsabackend.views.job_templates.Organization.objects.get')
    def test_get_job_template_table_data_valid_query(self, get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        qs = MagicMock(spec=QuerySet)
        filter.return_value = qs
        

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplates?search=bob&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_job_template_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        qs.filter.assert_called_with(Q(name__icontains='bob') | Q(description__icontains='bob')) 

    @patch('hsabackend.views.job_templates.JobTemplate.objects.filter')
    @patch('hsabackend.views.job_templates.Organization.objects.get')
    def test_get_job_template_table_data_valid_empty_query(self, get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Mock(spec=Organization)
        org.pk = 1
        get.return_value = org
        filter.return_value = MagicMock(spec=QuerySet)
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplates?search&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_job_template_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        filter.assert_called_with(organization=1)
    
    def test_get_job_individual_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplate/1')

        response = get_job_template_individual_data(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.job_templates.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates.Organization.objects.get')
    def test_get_job_template_individual_data_job_not_found(self, org, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        job.return_value = None
        org.return_value = Organization()

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplate/1')
        request.user = mock_user  

        response = get_job_template_individual_data(request, 1)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    @patch('hsabackend.views.job_templates.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates.Organization.objects.get')
    def test_get_job_template_individual_data_valid(self, get_org, get_job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org = Mock(spec=Organization)
        org.pk = 1
        get_org.return_value = org

        mock_response = {
            "id": 1,
            "name": "",
            "description": "",
        }

        job = Mock(spec=JobTemplate)
        job.pk = 1
        job.json.return_value = mock_response
        get_job.return_value = job

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplate/1')
        request.user = mock_user  

        response = get_job_template_individual_data(request, 1)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"] == mock_response

    def test_create_job_template_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate')
        request.user = mock_user  
        response = create_job_template(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.job_templates.Organization.objects.get')
    def test_create_job_template_auth_invalid(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate',
            data={
                "name": "",
                "description": "",
                "services": [
                    {
                        "id": 2
                    }
                ],
                "materials": [
                    {
                        "id": 2,
                        "unitsUsed": 0,
                        "pricePerUnit": "0.00"
                    },
                    {
                        "id": 4,
                        "unitsUsed": 0,
                        "pricePerUnit": "0.00"
                    }
                ]
            })
        request.user = mock_user  
        response = create_job_template(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.job_templates.Organization.objects.get')
    @patch('hsabackend.views.job_templates.Service.objects.get')
    @patch('hsabackend.views.job_templates.Material.objects.get')
    @patch('hsabackend.views.job_templates.JobTemplate')
    @patch('hsabackend.views.job_templates.JobTemplateService')
    @patch('hsabackend.views.job_templates.JobTemplateMaterial')
    def test_calls_save_if_valid(self, job_material, job_service, job_name, material, service, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org.return_value = Organization()
        service.return_value = Service()
        material.return_value = Material()

        job_name_obj = MagicMock(spec=JobTemplate)
        job_name.return_value = job_name_obj

        job_service_obj = MagicMock(spec=JobTemplateService)
        job_service.return_value = job_service_obj

        job_material_obj = MagicMock(spec=JobTemplateMaterial)
        job_material.return_value = job_material_obj
        
        factory = APIRequestFactory()

        mock_data = {
                "name": "",
                "description": "",
                "services": [
                    {
                        "id": 2
                    }
                ],
                "materials": [
                    {
                        "id": 2,
                        "unitsUsed": 0,
                        "pricePerUnit": "0.00"
                    },
                    {
                        "id": 4,
                        "unitsUsed": 0,
                        "pricePerUnit": "0.00"
                    }
                ]
            }

        request = factory.post('api/create/jobtemplate', data=mock_data, format='json')
        request.user = mock_user   
        response = create_job_template(request)

        job_name_obj.save.assert_called_once()

        assert job_service_obj.save.call_count == len(mock_data["services"])
        assert job_material_obj.save.call_count == len(mock_data["materials"])

        assert response.status_code == status.HTTP_201_CREATED

    def test_edit_job_template_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/jobtemplate/1')
        request.user = mock_user  
        response = edit_job_template(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.job_templates.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates.Organization.objects.get')
    def test_edit_job_template_not_found(self,org, job_name):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_name.return_value = None
        org.return_value = Organization()
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/jobtemplate/0')
        request.user = mock_user  
        response = edit_job_template(request, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.job_templates.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates.Organization.objects.get')
    def test_edit_job_template_invalid(self, org, job_name):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_job_name = MagicMock(spec=JobTemplate)
        job_name.return_value = mock_job_name
        org.return_value = Organization()
        
        mock_job_name.full_clean.side_effect = ValidationError({'description': ['This field is required.']})

        factory = APIRequestFactory()
        request = factory.post('/api/edit/jobtemplate/1',
            data={
                "name": "",
                "description": "",
            })
        request.user = mock_user  
        response = edit_job_template(request, 1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.job_templates.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates.Organization.objects.get')
    def test_edit_job_template_valid(self, org, job_name):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_job_name = MagicMock(spec=JobTemplate)
        job_name.return_value = mock_job_name
        org.return_value = Organization()

        factory = APIRequestFactory()
        request = factory.post('/api/edit/jobtemplate/1',
            data={
                "name": "",
                "description": "",
            })
        request.user = mock_user  
        response = edit_job_template(request, 1)
        
        assert response.status_code == status.HTTP_200_OK