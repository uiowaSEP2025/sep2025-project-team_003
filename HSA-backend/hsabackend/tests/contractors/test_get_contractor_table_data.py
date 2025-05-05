from unittest.mock import patch, Mock, MagicMock

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.contractors import get_contractor_table_data


class GetContractorTableDataTest(BaseTestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_contractor_table_no_offset(self, org):
        self.test_user.is_authenticated = True

        self.test_organization.is_onboarding = False
        org.return_value = self.test_organization

        factory = APIRequestFactory()
        request = factory.get('api/get/contractors')
        request.org = self.test_organization
        request.user = self.test_user
        res = get_contractor_table_data(request)
        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_contractor_table_offset_not_int(self, org):
        self.test_user.is_authenticated = True

        self.test_organization.is_onboarding = False
        org.return_value = self.test_organization

        factory = APIRequestFactory()
        request = factory.get('api/get/contractors?pagesize=10&offset=a')
        request.org = self.test_organization
        request.user = self.test_user
        res = get_contractor_table_data(request)
        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    def test_get_contractor_table_ok(self, filter, org):
        self.test_user.is_authenticated = True

        self.test_organization.is_onboarding = False
        org.return_value = self.test_organization

        mock_qs = MagicMock()
        filter.return_value = mock_qs

        factory = APIRequestFactory()
        request = factory.get('api/get/contractors?pagesize=10&offset=2')
        request.org = self.test_organization
        request.user = self.test_user
        res = get_contractor_table_data(request)
        assert res.status_code == 200
