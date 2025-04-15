from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.views.services import get_service_excluded_table_data, get_service_table_data, create_service, edit_service
from rest_framework.test import APITestCase
from hsabackend.models.organization import Organization
from django.db.models import QuerySet
from django.db.models import Q
from hsabackend.models.service import Service
from django.core.exceptions import ValidationError

class ServiceViewTest(APITestCase):
    def test_get_service_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/services?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = get_service_table_data(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    @patch('hsabackend.views.services.Organization.objects.get')
    def test_get_service_table_data_invalid(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        get.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/services?search')
        request.user = mock_user  
        response = get_service_table_data(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.services.Service.objects.filter')
    @patch('hsabackend.views.services.Organization.objects.get')
    def test_get_service_table_data_valid_query(self,get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        get.return_value = org
        qs = MagicMock(spec=QuerySet) # needed because it's sliced in the code
        filter.return_value = qs
        

        factory = APIRequestFactory()
        request = factory.get('/api/get/services?search=bob&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_service_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        qs.filter.assert_called_with(Q(service_name__icontains='bob') | Q(service_description__icontains='bob') ) 

    @patch('hsabackend.views.services.Service.objects.filter')
    @patch('hsabackend.views.services.Organization.objects.get')
    def test_get_service_table_data_valid_empty_query(self,get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Mock(spec=Organization)
        org.pk = 1
        org.is_onboarding = False
        get.return_value = org
        filter.return_value = MagicMock(spec=QuerySet)
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/services?search&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_service_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        filter.assert_called_with(organization=1) 
    
    def test_get_service_excluded_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/services/exclude?excludeIDs=1&search=bob&pagesize=5&offset=0')
        request.user = mock_user  
        response = get_service_excluded_table_data(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    @patch('hsabackend.views.services.Organization.objects.get')
    def test_get_service_excluded_table_data_invalid(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        get.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/services/exclude?excludeIDs=1&search')
        request.user = mock_user  
        response = get_service_excluded_table_data(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.services.Service.objects.exclude')
    @patch('hsabackend.views.services.Service.objects.filter')
    @patch('hsabackend.views.services.Organization.objects.get')
    def test_get_service_excluded_table_data_valid_query(self, get, filter, exclude):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        get.return_value = org
        qs = MagicMock(spec=QuerySet) # needed because it's sliced in the code
        filter.return_value = qs
        exclude.return_value = qs

        factory = APIRequestFactory()
        request = factory.get('/api/get/services/exclude?excludeIDs=1&search=bob&pagesize=20&offset=0')
        request.user = mock_user  
        response = get_service_excluded_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        qs.exclude.assert_called_with(id__in=[1])
        qs.filter.assert_not_called()

    @patch('hsabackend.views.services.Service.objects.filter')
    @patch('hsabackend.views.services.Organization.objects.get')
    def test_get_service_table_data_valid_empty_query(self,get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Mock(spec=Organization)
        org.pk = 1
        org.is_onboarding = False
        get.return_value = org
        filter.return_value = MagicMock(spec=QuerySet)
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/services/exclude?excludeIDs=1&search=bob&pagesize=5&offset=0')
        request.user = mock_user  
        response = get_service_excluded_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        filter.assert_called_with(organization=1) 

    def test_create_service_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('api/create/service')
        request.user = mock_user  
        response = create_service(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.services.Organization.objects.get')
    def test_create_service_auth_invalid(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        
        factory = APIRequestFactory()
        request = factory.post('api/create/service',
                data={
                    'service_name': 'Mow Lawn',
                    'service_description': 'Mowing the Lawn'
                })
        request.user = mock_user  
        response = create_service(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.services.Organization.objects.get')
    @patch('hsabackend.views.services.Service')
    def test_calls_save_if_valid(self, service_name, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        service_name_obj = MagicMock(spec=Service)
        service_name.return_value = service_name_obj
        
        factory = APIRequestFactory()
        request = factory.post('api/create/service',
                data={
                    'service_name': 'Mow Lawn',
                    'service_description': 'Mowing the Lawn'
                })
        request.user = mock_user   
        response = create_service(request)
        service_name_obj.save.assert_called_once()
        assert response.status_code == status.HTTP_201_CREATED

    def test_edit_service_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/service/1')
        request.user = mock_user  
        response = edit_service(request,1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.services.Service.objects.filter')
    @patch('hsabackend.views.services.Organization.objects.get')
    def test_edit_service_not_found(self,org, service_name):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        queryset = MagicMock()
        service_name.return_value = queryset
        queryset.exists.return_value = False
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/service/0')
        request.user = mock_user  
        response = edit_service(request, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.services.Service.objects.filter')
    @patch('hsabackend.views.services.Organization.objects.get')
    def test_edit_service_invalid(self,org, service_name):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        qs = MagicMock(spec=QuerySet)

        service_name.return_value = qs
        qs.exists.return_value = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        service_mock = MagicMock(name = 'serviceobj')
        qs.__getitem__.side_effect = lambda x: service_mock
        
        service_mock.full_clean.side_effect = ValidationError({'service_name': ['This field is required.']})

        factory = APIRequestFactory()
        request = factory.post('/api/edit/services/1',
                    data={
                        'service_name': 'Mow Lawn',
                        'service_description': 'Mowing the Lawn for free'
                    })
        request.user = mock_user  
        response = edit_service(request, 1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.services.Service.objects.filter')
    @patch('hsabackend.views.services.Organization.objects.get')
    def test_edit_service_invalid(self,org, service_name):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        qs = MagicMock(spec=QuerySet)

        service_name.return_value = qs
        qs.exists.return_value = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        service_mock = MagicMock(name = 'serviceobj')
        qs.__getitem__.side_effect = lambda x: service_mock
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/services/1',
                    data={
                        'service_name': 'Mow Lawn',
                        'service_description': 'Mowing the Lawn for free'
                    })
        request.user = mock_user  
        response = edit_service(request, 1)
        
        assert response.status_code == status.HTTP_200_OK

    def test_delete_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/service/1')
        request.user = mock_user  
        response = edit_service(request,1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.services.Service.objects.filter')
    @patch('hsabackend.views.services.Organization.objects.get')
    def test_delete_not_found(self, org, service_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        serivce_qs = MagicMock(spec=QuerySet)
        service_filter.return_value = serivce_qs
        serivce_qs.exists.return_value = False 
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/service/1')
        request.user = mock_user  
        response = edit_service(request,1)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.services.Service.objects.filter')
    @patch('hsabackend.views.services.Organization.objects.get')
    def test_delete_valid(self, org, service_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        serivce_qs = MagicMock(spec=QuerySet)
        service_filter.return_value = serivce_qs
        serivce_qs.exists.return_value = True 
        service_mock = MagicMock()
        serivce_qs.__getitem__.side_effect = lambda x: service_mock
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/service/1')
        request.user = mock_user  
        response = edit_service(request,1)
        
        assert response.status_code == status.HTTP_200_OK
        service_mock.delete.assert_called_once
