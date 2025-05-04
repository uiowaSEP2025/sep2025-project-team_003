from rest_framework.test import APITestCase
from unittest.mock import patch, Mock, MagicMock
from rest_framework.test import APIRequestFactory
from hsabackend.views.contractors import get_all_contractors_for_org, get_contractor_table_data, get_contractor_excluded_table_data, create_contractor, edit_contractor, delete_contractor
from hsabackend.models.organization import Organization
from django.core.exceptions import ValidationError

class TestGetAllContractors(APITestCase):
    
    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_contractors_ok(self, org, mock):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.get('api/get/all/contractors')
        request.org = mock_org
        request.user = mock_user

        res = get_all_contractors_for_org(request)
        assert res.status_code == 200
        mock.assert_called_once()

class TestGetContractorTableData(APITestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_contractor_table_no_offset(self, org):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.get('api/get/contractors')
        request.org = mock_org
        request.user = mock_user
        res = get_contractor_table_data(request)
        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_contractor_table_offset_not_int(self, org):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.get('api/get/contractors?pagesize=10&offset=a')
        request.org = mock_org
        request.user = mock_user
        res = get_contractor_table_data(request)
        assert res.status_code == 400

    
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    def test_get_contractor_table_ok(self, filter, org):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        mock_qs = MagicMock()
        filter.return_value = mock_qs
        
        factory = APIRequestFactory()
        request = factory.get('api/get/contractors?pagesize=10&offset=2')
        request.org = mock_org
        request.user = mock_user
        res = get_contractor_table_data(request)
        assert res.status_code == 200

class TestGetContractorExcluded(APITestCase):
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_contractor_table_no_offset(self, org):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.get('api/get/contractors/exclude')
        request.org = mock_org
        request.user = mock_user
        res = get_contractor_excluded_table_data(request)
        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_contractor_table_offset_not_int(self, org):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.get('api/get/contractors/exclude?pagesize=10&offset=a')
        request.org = mock_org
        request.user = mock_user
        res = get_contractor_excluded_table_data(request)
        assert res.status_code == 400

    
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    def test_get_contractor_table_ok(self, filter, org):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        mock_qs = MagicMock()
        filter.return_value = mock_qs
        
        factory = APIRequestFactory()
        request = factory.get('api/get/contractors/exclude?pagesize=10&offset=2')
        request.org = mock_org
        request.user = mock_user
        res = get_contractor_excluded_table_data(request)
        assert res.status_code == 200

class TestCreateContractor(APITestCase):
    @patch('hsabackend.views.contractors.Contractor')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_create_invalid_data(self,org, con):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
                
        mock = MagicMock()
        con.return_value = mock
        mock.full_clean.side_effect = ValidationError({'name': ['Error while saving organization']})

        factory = APIRequestFactory()
        request = factory.post('api/create/contractor')
        request.org = mock_org
        request.user = mock_user
        res = create_contractor(request)
        assert res.status_code == 400

    @patch('hsabackend.views.contractors.Contractor')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_create_ok(self,org, con):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
                
        mock = MagicMock()
        con.return_value = mock

        factory = APIRequestFactory()
        request = factory.post('api/create/contractor')
        request.org = mock_org
        request.user = mock_user
        res = create_contractor(request)
        mock.save.assert_called_once()
        assert res.status_code == 201

class TestEditContractor(APITestCase):
    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_not_found(self, org, con):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
                
        mock = MagicMock()
        mock.exists.return_value = False
        con.return_value = mock

        factory = APIRequestFactory()
        request = factory.post('api/edit/contractor')
        request.user = mock_user

        res = edit_contractor(request, 2)

        assert res.status_code == 404

    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_not_valid(self, org, con):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
                
        mock = MagicMock()
        mock.exists.return_value = True
        con.return_value = mock

        mock_cust = Mock(name="MockCust")
        mock.__getitem__.side_effect = lambda x: mock_cust

        mock_cust.full_clean.side_effect = ValidationError({'name': ['Error while saving organization']})

        factory = APIRequestFactory()
        request = factory.post('api/edit/contractor')
        request.user = mock_user

        res = edit_contractor(request, 2)
        assert res.status_code == 400

    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_ok(self, org, con):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
                
        mock = MagicMock()
        mock.exists.return_value = True
        con.return_value = mock

        mock_cust = Mock(name="MockCust")
        mock.__getitem__.side_effect = lambda x: mock_cust

        factory = APIRequestFactory()
        request = factory.post('api/edit/contractor')
        request.user = mock_user

        res = edit_contractor(request, 2)
        assert res.status_code == 200

class TestDelete(APITestCase):
    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_delete_not_found(self, org, con):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
                
        mock = MagicMock()
        mock.exists.return_value = False
        con.return_value = mock

        factory = APIRequestFactory()
        request = factory.post('api/delete/contractor/2')
        request.user = mock_user

        res = delete_contractor(request, 2)
        assert res.status_code == 404

    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_delete_ok(self, org, con):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
                
        mock = MagicMock()
        mock.exists.return_value = True
        con.return_value = mock

        factory = APIRequestFactory()
        request = factory.post('api/delete/contractor/2')
        request.user = mock_user

        res = delete_contractor(request, 2)
        assert res.status_code == 200
