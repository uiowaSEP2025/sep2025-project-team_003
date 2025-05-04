from django.test import TestCase
from rest_framework.test import APIRequestFactory
from hsabackend.views.user_auth import user_exist, user_create, login_view, logout_view
from unittest.mock import patch, Mock
class UserViewsTestCase(TestCase):

    def test_user_exist_with_no_username_or_email(self):
        factory = APIRequestFactory()
        request = factory.post('/api/userexist')

        response = user_exist(request)

        assert response.status_code == 400

    @patch('hsabackend.views.user_auth.User.objects.filter')
    def test_user_exist(self, filter):
        factory = APIRequestFactory()
        request = factory.post('/api/userexist')

        mock_queryset = Mock()
        mock_queryset.exists.return_value = False
        filter.return_value = mock_queryset

        response = user_exist(request)

        assert response.status_code == 409

    @patch('hsabackend.views.user_auth.User.objects.filter')
    def test_user_exist(self, filter):
        factory = APIRequestFactory()
        request = factory.post('/api/userexist')

        mock_queryset = Mock()
        mock_queryset.exists.return_value = False
        filter.return_value = mock_queryset

        response = user_exist(request)

        assert response.status_code == 200

    def test_user_create_missing_organization_info(self):
        pass

    def test_user_create_with_existing_user(self):
        pass

    def test_user_create_password_not_strong_enough(self):
        pass

    def test_bad_org_data(self):
        pass

    def test_user_create_successful(self):
        pass

    def test_login_successful(self):
        pass

    def test_login_failed_invalid_credentials(self):
        pass

    def test_logout_successful(self):
        pass

    def test_logout_failed_not_logged_in(self):
        pass
