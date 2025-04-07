from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.views.job_templates_materials import delete_cached_job_template_material, get_job_template_material_table_data, create_job_template_material, delete_job_template_material
from rest_framework.test import APITestCase
from hsabackend.models.organization import Organization
from django.db.models import QuerySet
from django.db.models import Q
from hsabackend.models.material import Material
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.job_template_material import JobTemplateMaterial
from django.core.exceptions import ValidationError

class materialViewTest(APITestCase):
    def test_get_job_template_material_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplate/1/materials?pagesize=100&offset=0')
        request.user = mock_user  
        response = get_job_template_material_table_data(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @patch('hsabackend.views.job_templates_materials.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_materials.Material.objects.get')
    @patch('hsabackend.views.job_templates_materials.Organization.objects.get')
    def test_get_job_template_material_table_data_invalid(self, org, material, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job.return_value = JobTemplate()
        material.return_value = Material()
        org.return_value = Organization()
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplate/1/materials?pagesize')
        request.user = mock_user  
        response = get_job_template_material_table_data(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.job_templates_materials.Material.objects.get')
    @patch('hsabackend.views.job_templates_materials.Organization.objects.get')
    def test_get_job_template_material_table_job_template_not_found(self, org, material):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        material.return_value = Material()
        org.return_value = Organization()

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplate/1/materials?pagesize=100&offset=10')
        request.user = mock_user  
        response = get_job_template_material_table_data(request, 1)
        assert response.status_code == status.HTTP_404_NOT_FOUND


    @patch('hsabackend.views.job_templates_materials.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_materials.Organization.objects.get')
    def test_get_job_template_table_data_valid_empty_query(self, org, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job.return_value = JobTemplate()
        org.return_value = Organization()
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobtemplate/1/materials?pagesize=10&offset=10')
        request.user = mock_user  
        response = get_job_template_material_table_data(request, 1)
        
        assert response.status_code == status.HTTP_200_OK

    def test_job_template_create_material_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate/1/material')
        request.user = mock_user  
        response = create_job_template_material(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.job_templates_materials.JobTemplateMaterial.objects.filter')
    @patch('hsabackend.views.job_templates_materials.Material.objects.get')
    @patch('hsabackend.views.job_templates_materials.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_materials.Organization.objects.get')
    def test_job_template_create_material_auth_invalid(self, org, job, material, job_material_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_material_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = True

        material.return_value = Material()
        job.return_value = JobTemplate()
        org.return_value = Organization()

        mockdata = {
            "materials": [
                {
                    'id': 2,
                    'units_used': 1,
                    'price_per_unit': 0.00
                },
                {
                    'id': 4,
                    'units_used': 1,
                    'price_per_unit': 0.00
                }
            ]
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate/1/material', data=mockdata, format='json')
        request.user = mock_user  
        response = create_job_template_material(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.job_templates_materials.JobTemplateMaterial.objects.filter')
    @patch('hsabackend.views.job_templates_materials.Material.objects.get')
    @patch('hsabackend.views.job_templates_materials.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_materials.Organization.objects.get')
    def test_job_template_create_material_request_empty(self, org, job, material, job_material_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_material_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = True

        material.return_value = Material()
        job.return_value = JobTemplate()
        org.return_value = Organization()

        mockdata = {
            "materials": []
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate/1/material', data=mockdata, format='json')
        request.user = mock_user  
        response = create_job_template_material(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.job_templates_materials.JobTemplateMaterial.objects.filter')
    @patch('hsabackend.views.job_templates_materials.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_materials.Organization.objects.get')
    @patch('hsabackend.views.job_templates_materials.Material.objects.get')
    @patch('hsabackend.views.job_templates_materials.JobTemplateMaterial')
    def test_job_template_create_material_entry_already_exist(self, job_material, material, org, job, job_material_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_material_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = True

        job.return_value = JobTemplate()
        org.return_value = Organization()
        material.return_value = Material()
        job_material_obj = MagicMock(spec=JobTemplateMaterial)
        job_material.return_value = job_material_obj

        mockdata = {
            "materials": [
                {
                    'id': 2,
                    'units_used': 1,
                    'price_per_unit': 0.00
                },
                {
                    'id': 4,
                    'units_used': 1,
                    'price_per_unit': 0.00
                }
            ]
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate/1/material', data=mockdata, format='json')
        request.user = mock_user

        response = create_job_template_material(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.job_templates_materials.JobTemplateMaterial.objects.filter')
    @patch('hsabackend.views.job_templates_materials.JobTemplate.objects.get')
    @patch('hsabackend.views.job_templates_materials.Organization.objects.get')
    @patch('hsabackend.views.job_templates_materials.Material.objects.get')
    @patch('hsabackend.views.job_templates_materials.JobTemplateMaterial')
    def test_calls_save_if_valid(self, job_material, material, org, job, job_material_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_material_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = False

        job.return_value = JobTemplate()
        org.return_value = Organization()
        material.return_value = Material()
        job_material_obj = MagicMock(spec=JobTemplateMaterial)
        job_material.return_value = job_material_obj

        mockdata = {
            "materials": [
                {
                    'id': 2,
                    'unitsUsed': 1,
                    'pricePerUnit': 0.00
                },
                {
                    'id': 4,
                    'unitsUsed': 1,
                    'pricePerUnit': 0.00
                }
            ]
        }
        
        factory = APIRequestFactory()
        request = factory.post('api/create/jobtemplate/1/material', data=mockdata, format='json')
        request.user = mock_user

        response = create_job_template_material(request, 1)
        job_material_obj.save.call_count == len(mockdata["materials"])
        assert response.status_code == status.HTTP_201_CREATED

    def test_job_template_delete_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/jobtemplate/1/material/1')
        request.user = mock_user  
        response = delete_job_template_material(request, 1, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.job_templates_materials.JobTemplateMaterial.objects.filter')
    @patch('hsabackend.views.job_templates_materials.Organization.objects.get')
    def test_job_template_delete_not_found(self, org, job_material_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_material_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = False 
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/jobtemplate/1/material/1')
        request.user = mock_user  
        response = delete_job_template_material(request, 1, 1)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.job_templates_materials.JobTemplateMaterial.objects.filter')
    @patch('hsabackend.views.job_templates_materials.Organization.objects.get')
    def test_delete_valid(self, org, job_material_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        job_serivce_qs = MagicMock(spec=QuerySet)
        job_material_filter.return_value = job_serivce_qs
        job_serivce_qs.exists.return_value = True 
        material_mock = MagicMock()
        job_serivce_qs.__getitem__.side_effect = lambda x: material_mock
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/jobtemplate/1/material/1')
        request.user = mock_user  
        response = delete_job_template_material(request, 1, 1)
        
        assert response.status_code == status.HTTP_200_OK
        material_mock.delete.assert_called_once

    def test_delete_cached_invalid(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mockdata = {
            "jobTemplateMaterials": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ],
        }
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/jobtemplate/1/materials', data=mockdata, format='json')
        request.user = mock_user  
        response = delete_cached_job_template_material(request, 1)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.job_templates_materials.JobTemplateMaterial.objects.get')
    def test_delete_cached_valid(self, job_material):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        job_material_obj = MagicMock(spec=JobTemplateMaterial)
        job_material.return_value = job_material_obj

        mockdata = {
            "jobTemplateMaterials": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ],
        }
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/jobtemplate/1/materials', data=mockdata, format='json')
        request.user = mock_user  
        response = delete_cached_job_template_material(request, 1)
        
        assert response.status_code == status.HTTP_200_OK
        assert job_material_obj.delete.call_count == len(mockdata["jobTemplateMaterials"])
    
