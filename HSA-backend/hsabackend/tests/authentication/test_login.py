from unittest.mock import patch, MagicMock

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from hsabackend.views.user_auth import login_view, logout_view


class LoginTest(TestCase):
    @patch('hsabackend.views.user_auth.authenticate')
    @patch('hsabackend.views.user_auth.login')
    def test_login_successful(self, login, authenticate):
        factory = APIRequestFactory()
        request = factory.post('/api/login')
        authenticate.return_value = True

        response = login_view(request)

        assert response.status_code == 200

    @patch('hsabackend.views.user_auth.authenticate')
    @patch('hsabackend.views.user_auth.login')
    def test_login_failed_invalid_credentials(self, login, authenticate):
        factory = APIRequestFactory()
        request = factory.post('/api/login')
        authenticate.return_value = False

        response = login_view(request)

        assert response.status_code == 401
