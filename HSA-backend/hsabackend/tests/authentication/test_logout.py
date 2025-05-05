from unittest.mock import patch, MagicMock

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from hsabackend.views.user_auth import logout_view

class LogoutTest(TestCase):
    @patch('hsabackend.views.user_auth.logout')
    def test_logout_successful(self,sess):
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        factory = APIRequestFactory()
        request = factory.post("api/logout",)
        request.user = mock_user

        respose = logout_view(request)
        assert respose.status_code == 200

    @patch('hsabackend.views.user_auth.logout')
    def test_logout_failed_not_logged_in(self, logout):
        mock_user = MagicMock()
        mock_user.is_authenticated = False
        factory = APIRequestFactory()
        request = factory.post("api/logout",)
        request.user = mock_user
        request.session = ''

        respose = logout_view(request)
        assert respose.status_code == 400
