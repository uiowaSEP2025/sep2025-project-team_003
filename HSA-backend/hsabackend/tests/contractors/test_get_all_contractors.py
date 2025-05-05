from unittest.mock import patch, Mock

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.contractors import get_all_contractors_for_org


class GetAllContractorsTest(BaseTestCase):

    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_contractors_ok(self, org, mock):
        self.test_user.is_authenticated = True

        self.test_organization.is_onboarding = False
        org.return_value = self.test_organization

        factory = APIRequestFactory()
        request = factory.get('api/get/all/contractors')
        request.org = self.test_organization
        request.user = self.test_user

        res = get_all_contractors_for_org(request)
        assert res.status_code == 200
        mock.assert_called_once()
