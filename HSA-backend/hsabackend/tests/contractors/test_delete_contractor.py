from unittest.mock import patch, Mock, MagicMock

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.contractors import delete_contractor


class DeleteContractorTest(BaseTestCase):
    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_delete_not_found(self, org, con):

        self.test_organization.is_onboarding = False
        org.return_value = self.test_organization

        mock = MagicMock()
        mock.exists.return_value = False
        con.return_value = mock

        factory = APIRequestFactory()
        request = factory.post('api/delete/contractor/2')
        request.user = self.test_user
        self.force_authenticate_user(request)

        res = delete_contractor(request, 2)
        assert res.status_code == 404

    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_delete_ok(self, org, con):

        self.test_organization.is_onboarding = False
        org.return_value = self.test_organization

        mock = MagicMock()
        mock.exists.return_value = True
        con.return_value = mock

        factory = APIRequestFactory()
        request = factory.post('api/delete/contractor/1')
        request.user = self.test_user
        self.force_authenticate_user(request)

        res = delete_contractor(request, 1)
        assert res.status_code == 200
