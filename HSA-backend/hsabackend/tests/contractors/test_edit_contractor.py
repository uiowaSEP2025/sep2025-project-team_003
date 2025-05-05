from unittest.mock import patch, Mock, MagicMock

from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from hsabackend.models.contractor import Contractor
from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.contractors import edit_contractor


class EditContractorTest(BaseTestCase):
    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_not_found(self, org, con):
        # Use the test_user created in setUpTestData
        org.return_value = self.test_organization

        mock = MagicMock()
        mock.exists.return_value = False
        con.return_value = mock

        factory = APIRequestFactory()
        request = factory.post('api/edit/contractor')
        request.user = self.test_user

        res = edit_contractor(request, 2)

        assert res.status_code == 404

    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_not_valid(self, org, con):
        # Use the test_user and test_organization created in setUpTestData
        org.return_value = self.test_organization

        mock = MagicMock()
        mock.exists.return_value = True
        con.return_value = mock

        mock_cust = Mock(name="MockCust")
        mock.__getitem__.side_effect = lambda x: mock_cust

        mock_cust.full_clean.side_effect = ValidationError({'name': ['Error while saving organization']})

        factory = APIRequestFactory()
        request = factory.post('api/edit/contractor')
        request.user = self.test_user

        res = edit_contractor(request, 2)
        assert res.status_code == 400

    @patch('hsabackend.views.contractors.Contractor.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_ok(self, org, con):
        # Use the test_user and test_organization created in setUpTestData
        org.return_value = self.test_organization

        mock = MagicMock()
        mock.exists.return_value = True
        con.return_value = mock

        mock_cust = Mock(name="MockCust")
        mock.__getitem__.side_effect = lambda x: mock_cust

        factory = APIRequestFactory()
        request = factory.post('api/edit/contractor', {
        "first_name" : "bob",
        "last_name" : "parson",
        "email" : "bparson@bparson.com",
        "phone" : "123-456-7890",
        "organization": self.test_organization,
        })
        request.user = self.test_user

        # Fix the variable name from mock_con to mock
        res = edit_contractor(request, mock.pk)
        assert res.status_code == 200
