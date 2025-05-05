from django.test import TestCase
from rest_framework.test import APIRequestFactory
from hsabackend.views.user_auth import user_exist, user_create, login_view, logout_view
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError

class UserCreateTest(TestCase):
    @patch('hsabackend.views.user_auth.User.objects.filter')
    def test_user_create_missing_organization_info(self, filter):
        factory = APIRequestFactory()
        request = factory.post('/api/api/create/user')

        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = False
        filter.return_value = mock_queryset

        response = user_create(request)

        assert response.status_code == 400

    @patch('hsabackend.views.user_auth.User.objects.filter')
    def test_user_create_with_existing_user(self, filter):
        factory = APIRequestFactory()
        request = factory.post('/api/api/create/user', data={"organizationInfo": {"c":"a"}, "username": 'gg9192', "email": "aguo2@uiowa.edu"}, format="json")

        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = True
        filter.return_value = mock_queryset

        response = user_create(request)
        assert response.status_code == 409

    @patch('hsabackend.views.user_auth.password_strength_validator')
    @patch('hsabackend.views.user_auth.User.objects.filter')
    def test_user_create_password_not_strong_enough(self, filter, pw):
        factory = APIRequestFactory()
        request = factory.post('/api/api/create/user', data={"organizationInfo": {"c":"a"}, "username": 'gg9192', "email": "aguo2@uiowa.edu"}, format="json")

        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = False
        filter.return_value = mock_queryset

        pw.return_value = False
        response = user_create(request)

        assert response.status_code == 400

    @patch('hsabackend.views.user_auth.password_strength_validator')
    @patch('hsabackend.views.user_auth.User.objects.filter')
    @patch('hsabackend.views.user_auth.Organization')
    def test_bad_org_data(self, org, filter, pw):
        factory = APIRequestFactory()
        request = factory.post('/api/api/create/user', data={"organizationInfo": {"c":"a"}, "username": 'gg9192', "email": "aguo2@uiowa.edu"}, format="json")

        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = False
        filter.return_value = mock_queryset

        pw.return_value = False

        mock_org = MagicMock()
        mock_org.save.side_effect = ValidationError("Error while saving organization")

        org.return_value = mock_org

        response = user_create(request)

        assert response.status_code == 400

    @patch('hsabackend.views.user_auth.password_strength_validator')
    @patch('hsabackend.views.user_auth.User.objects.filter')
    @patch('hsabackend.views.user_auth.Organization')
    def test_user_create_unsuccessful(self, org, filter, pw):
        factory = APIRequestFactory()
        request = factory.post('/api/api/create/user', data={"organizationInfo": {"c":"a"}, "username": 'gg9192', "email": "aguo2@uiowa.edu"}, format="json")

        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = False
        filter.return_value = mock_queryset

        pw.return_value = True

        mock_org = MagicMock()
        mock_org.save.side_effect = ValidationError("Error while saving organization")

        org.return_value = mock_org

        response = user_create(request)

        assert response.status_code == 400


    @patch('hsabackend.views.user_auth.password_strength_validator')
    @patch('hsabackend.views.user_auth.User.objects.filter')
    @patch('hsabackend.views.user_auth.Organization')
    def test_user_create_successful(self, org, filter, pw):
        factory = APIRequestFactory()
        request = factory.post('/api/api/create/user', data={"organizationInfo": {"c":"a"}, "username": 'gg9192', "email": "aguo2@uiowa.edu"}, format="json")

        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = False
        filter.return_value = mock_queryset

        pw.return_value = True

        mock_org = MagicMock(name="sie")

        org.return_value = mock_org

        response = user_create(request)

        assert response.status_code == 201
        mock_org.full_clean.assert_called_once()
        mock_org.save.assert_called_once()
