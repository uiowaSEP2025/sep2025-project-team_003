from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.db.models import QuerySet
from django.db.models import Q
from unittest.mock import call
from django.core.exceptions import ValidationError
from hsabackend.views.organizations import createOrganization, deleteOrganization, getOrganizationDetail, editOrganizationDetail
from hsabackend.models.organization import Organization

class orgViewTests(APITestCase):
    # def test_unauth_user_attacks_all_endpoints(self):
    #     mock_user = Mock(spec=User)
    #     mock_user.is_authenticated = False
    #     factory = APIRequestFactory()

    #     # get org test
    #     request = factory.get('/api/get/organization')
    #     request.user = mock_user  
    #     response = getOrganizationDetail(request)
        
    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED

    #     # create organization test
    #     request = factory.post('/api/create/organization')
    #     request.user = mock_user  
    #     response = createOrganization(request)

    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED

    #     # edit organization test
    #     request = factory.post('/api/edit/organization')
    #     request.user = mock_user  
    #     response = editOrganizationDetail(request)

    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED

    #     # delete organization test
    #     request = factory.post('/api/delete/organization')
    #     request.user = mock_user  
    #     response = deleteOrganization(request)

    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # @patch('hsabackend.views.organizations.Organization.objects.get')
    # def test_auth_org_retrive_works(self, org):
    #     mock_user = Mock(spec=User)
    #     mock_user.is_authenticated = True

    #     factory = APIRequestFactory()

    #     org_object = MagicMock(spec=Organization)
    #     org.json.return_value = {}
    #     org.return_value = org_object

    #     request = factory.get('api/get/organization')
    #     request.user = mock_user
    #     response = getOrganizationDetail(request)
        
    #     assert response.status_code == status.HTTP_200_OK

    @patch('hsabackend.utils.auth_wrapper.Organization')
    @patch('hsabackend.views.organizations.Organization')
    def test_create_org_if_auth_and_valid(self, org1,org2):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        factory = APIRequestFactory()

        org_object = MagicMock(spec=Organization)
        manager = MagicMock()
        org1.objects = manager
        manager.get.return_value = org_object

        manager1 = MagicMock()
        org2.objects = manager1


        qs = MagicMock(spec=QuerySet, name="shit")
        manager.filter.return_value = qs
        qs.count.return_value = 0

        mock_data = {
            "name": "Superman HQ",
            "email": "supermanHQ@supermanHQ.co",
            "city": "BobTown",
            "requestor_state": "Iowa",
            "requestor_zip": "52213",
            "requestor_address": "222 Box",
            "ownerFn": "Dov",
            "ownerLn": "Sob"
        }

        request = factory.post('api/create/organization', data=mock_data, format='json')
        request.user = mock_user
        response = createOrganization(request)

        org_object.save.assert_called_once()
        
        assert response.status_code == status.HTTP_201_CREATED


    # @patch('hsabackend.views.organizations.Organization.objects.filter')
    # @patch('hsabackend.views.organizations.Organization.objects.get')
    # def test_create_org_fail_if_already_has_org(self, org, filter):
    #     mock_user = Mock(spec=User)
    #     mock_user.is_authenticated = True

    #     factory = APIRequestFactory()

    #     org_object = MagicMock(spec=Organization)
    #     org.return_value = org_object

    #     qs = MagicMock(spec=QuerySet)
    #     qs.count.return_value = 1 # no prev account
    #     filter.return_value = qs

    #     request = factory.post('api/create/organization', format='json')
    #     request.user = mock_user
    #     response = createOrganization(request)
        
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert response.data.get('errors', '') == "This user already has an organization"


    # @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    # @patch('hsabackend.views.organizations.Organization')
    # def test_create_org_fail_if_missing_data(self, org_construct, auth_org):
    #     mock_user = MagicMock(spec=User)
    #     mock_user.is_authenticated = True

    #     org = Organization()
    #     org.is_onboarding = False
    #     auth_org.return_value = org

    #     factory = APIRequestFactory()

    #     qs = MagicMock(spec=QuerySet, name="filter qs")
    #     qs.count.return_value = 0

    #     manager = MagicMock(name="manager")

    #     org_construct.objects = manager
    #     manager.filter.return_value = qs

    #     # Mock instance
    #     org_instance = MagicMock()
    #     org_construct.return_value = org_instance
    #     org_instance.full_clean.side_effect = ValidationError({'email': ['This field is required.']})

    #     mock_data = {
    #         "city": "BobTown",
    #         "requestor_state": "Iowa",
    #         "requestor_zip": "52213",
    #         "requestor_address": "222 Box",
    #         "ownerLn": "Sob"
    #     }

    #     request = factory.post('api/create/organization', data=mock_data, format='json')
    #     request.user = mock_user
    #     response = createOrganization(request)

    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert response.data.get('errors', '') == {'email': ['This field is required.']}


    # @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    # def test_edit_org_succeeds(self, org):
    #     mock_user = Mock(spec=User)
    #     mock_user.is_authenticated = True

    #     factory = APIRequestFactory()

    #     org_object = MagicMock(spec=Organization)
    #     org.return_value = org_object

    #     mock_data = {
    #         "name": "Superman HQ",
    #         "email": "supermanHQ@supermanHQ.co",
    #         "city": "BobTown",
    #         "requestor_address": "222 Box",
    #         "ownerFn": "Dov",
    #         "ownerLn": "Sob",
    #         "is_onboarding": False,
    #     }

    #     request = factory.post('api/edit/organization', data=mock_data, format='json')
    #     request.user = mock_user
    #     response = editOrganizationDetail(request)

    #     org_object.save.assert_called_once()
        
    #     assert response.status_code == status.HTTP_200_OK


    # @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    # def test_edit_org_fail_if_bogus_param(self, org):
    #     mock_user = Mock(spec=User)
    #     mock_user.is_authenticated = True

    #     factory = APIRequestFactory()

    #     org_object = MagicMock(spec=Organization, name="Org")
    #     org_object.is_onboarding = False
    #     org.return_value = org_object
    #     org_object.full_clean.side_effect = ValidationError({'email': ['Invalid Email']})

    #     mock_data = {
    #         "name": "Superman HQ",
    #         "email": "oofemail",
    #         "city": "BobTown",
    #         "requestor_address": "222 Box",
    #         "ownerFn": "Dov",
    #         "ownerLn": "Sob"
    #     }

    #     request = factory.post('api/edit/organization', data=mock_data, format='json')
    #     request.user = mock_user
    #     response = editOrganizationDetail(request)
        
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert response.data.get("errors", "") == {'email': ['Invalid Email']}


    # @patch('hsabackend.views.organizations.Organization.objects.filter')
    # @patch('hsabackend.views.organizations.Organization')
    # def test_delete_org_fails(self, org, filter):
    #     mock_user = Mock(spec=User)
    #     mock_user.is_authenticated = True

    #     factory = APIRequestFactory()

    #     org_object = MagicMock(spec=Organization)
    #     org.return_value = org_object

    #     qs = MagicMock(spec=QuerySet)
    #     qs.count.return_value = 0 # no prev account
    #     filter.return_value = qs

    #     request = factory.post('api/delete/organization', format='json')
    #     request.user = mock_user
    #     response = deleteOrganization(request)
        
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert response.data.get('errors', '') == "All users must have at least 1 org; You only have 1 or less orgs, cannot delete."

