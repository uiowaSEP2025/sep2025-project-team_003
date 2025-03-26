from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.views.materials import get_material_excluded_table_data, get_material_table_data, create_material, edit_material
from rest_framework.test import APITestCase
from hsabackend.models.organization import Organization
from django.db.models import QuerySet
from django.db.models import Q
from hsabackend.models.material import Material
from django.core.exceptions import ValidationError

class materialViewTest(APITestCase):
    def test_get_material_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = get_material_table_data(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    @patch('hsabackend.views.materials.Organization.objects.get')
    def test_get_material_table_data_invalid(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search')
        request.user = mock_user  
        response = get_material_table_data(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.materials.Material.objects.filter')
    @patch('hsabackend.views.materials.Organization.objects.get')
    def test_get_material_table_data_valid_query(self,get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        qs = MagicMock(spec=QuerySet)
        filter.return_value = qs
        

        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search=bob&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_material_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        qs.filter.assert_called_with(Q(material_name__icontains='bob')) 

    @patch('hsabackend.views.materials.Material.objects.filter')
    @patch('hsabackend.views.materials.Organization.objects.get')
    def test_get_material_table_data_valid_empty_query(self,get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Mock(spec=Organization)
        org.pk = 1
        get.return_value = org
        filter.return_value = MagicMock(spec=QuerySet)
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_material_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        filter.assert_called_with(organization=1)

    def test_get_material_excluded_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials/exclude?excludeIDs=1&search=bob&pagesize=5&offset=0')
        request.user = mock_user  
        response = get_material_excluded_table_data(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    @patch('hsabackend.views.materials.Organization.objects.get')
    def test_get_material_excluded_table_data_invalid(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials/exclude?excludeIDs=1&search')
        request.user = mock_user  
        response = get_material_excluded_table_data(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.materials.Material.objects.exclude')
    @patch('hsabackend.views.materials.Material.objects.filter')
    @patch('hsabackend.views.materials.Organization.objects.get')
    def test_get_material_excluded_table_data_valid_query(self, get, filter, exclude):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        qs = MagicMock(spec=QuerySet) # needed because it's sliced in the code
        filter.return_value = qs
        exclude.return_value = qs

        factory = APIRequestFactory()
        request = factory.get('/api/get/materials/exclude?excludeIDs=1&search=bob&pagesize=20&offset=0')
        request.user = mock_user  
        response = get_material_excluded_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        qs.exclude.assert_called_with(id__in=[1])
        qs.filter.assert_not_called()

    @patch('hsabackend.views.materials.Material.objects.filter')
    @patch('hsabackend.views.materials.Organization.objects.get')
    def test_get_material_table_data_valid_empty_query(self,get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Mock(spec=Organization)
        org.pk = 1
        get.return_value = org
        filter.return_value = MagicMock(spec=QuerySet)
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials/exclude?excludeIDs=1&search=bob&pagesize=5&offset=0')
        request.user = mock_user  
        response = get_material_excluded_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        filter.assert_called_with(organization=1) 

    def test_create_material_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('api/create/material')
        request.user = mock_user  
        response = create_material(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.materials.Organization.objects.get')
    def test_create_material_auth_invalid(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        
        factory = APIRequestFactory()
        request = factory.post('api/create/material',
                data={
                    'material_name': 'Test Material',
                })
        request.user = mock_user  
        response = create_material(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.materials.Organization.objects.get')
    @patch('hsabackend.views.materials.Material')
    def test_calls_save_if_valid(self, material_name, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        material_name_obj = MagicMock(spec=Material)
        material_name.return_value = material_name_obj
        
        factory = APIRequestFactory()
        request = factory.post('api/create/material',
                data={
                    'material_name': 'Test Material',
                })
        request.user = mock_user   
        response = create_material(request)
        material_name_obj.save.assert_called_once()
        assert response.status_code == status.HTTP_201_CREATED

    def test_edit_material_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/material/1')
        request.user = mock_user  
        response = edit_material(request, 1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.materials.Material.objects.get')
    @patch('hsabackend.views.materials.Organization.objects.get')
    def test_edit_material_not_found(self,org, material_name):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        material_name.return_value = None
        org.return_value = Organization()
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/material/0')
        request.user = mock_user  
        response = edit_material(request, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.materials.Material.objects.get')
    @patch('hsabackend.views.materials.Organization.objects.get')
    def test_edit_material_invalid(self,org, material_name):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_material_name = MagicMock(spec=Material)
        material_name.return_value = mock_material_name
        org.return_value = Organization()
        mock_material_name.full_clean.side_effect = ValidationError({'material_name': ['This field is required.']})

        factory = APIRequestFactory()
        request = factory.post('/api/edit/materials/1',
                    data={
                        'material_name': 'Test More Material',
                    })
        request.user = mock_user  
        response = edit_material(request, 1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.materials.Material.objects.get')
    @patch('hsabackend.views.materials.Organization.objects.get')
    def test_edit_material_valid(self,org, material_name):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_material_name = MagicMock(spec=Material)
        material_name.return_value = mock_material_name
        org.return_value = Organization()

        factory = APIRequestFactory()
        request = factory.post('/api/edit/materials/1',
                    data={
                        'material_name': 'Test More Material',
                    })
        request.user = mock_user  
        response = edit_material(request, 1)
        
        assert response.status_code == status.HTTP_200_OK