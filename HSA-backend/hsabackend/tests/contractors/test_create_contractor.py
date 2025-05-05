from unittest.mock import patch, Mock, MagicMock

from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.contractors import create_contractor


class CreateContractorTest(BaseTestCase):
    @patch('hsabackend.views.contractors.Contractor')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_create_invalid_data(self, org, con):
        self.test_organization.is_onboarding = False
        org.return_value = self.test_organization

        mock = MagicMock()
        con.return_value = mock
        mock.full_clean.side_effect = ValidationError({'name': ['Error while saving organization']})

        factory = APIRequestFactory()
        request = factory.post('api/create/contractor')
        request.org = self.test_organization
        request.user = self.test_user
        self.force_authenticate_user(request)
        res = create_contractor(request)
        assert res.status_code == 400

    @patch('hsabackend.views.contractors.Contractor')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_create_ok(self, org, con):
        self.test_organization.is_onboarding = False
        org.return_value = self.test_organization

        mock = MagicMock()
        con.return_value = mock

        factory = APIRequestFactory()
        request = factory.post('api/create/contractor', {
        "firstName" : "bob",
        "lastName" : "parson",
        "email" : "bob@bobby.com",
        "phone" : "123-456-7890",
        "organization": self.test_organization,
        })
        request.user = self.test_user
        self.force_authenticate_user(request)
        res = create_contractor(request)
        assert res.status_code == 201
