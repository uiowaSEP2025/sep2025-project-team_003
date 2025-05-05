from django.test import TestCase
from rest_framework.test import APIRequestFactory
from hsabackend.views.user_auth import user_exist, user_create, login_view, logout_view
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError

class UserExistsTest(TestCase):

    def test_user_exist_with_no_username_or_email(self):
        factory = APIRequestFactory()
        request = factory.post('/api/userexist')

        response = user_exist(request)

        assert response.status_code == 400

    @patch('hsabackend.views.user_auth.User.objects.filter')
    def test_user_exist(self, filter):
        factory = APIRequestFactory()
        request = factory.post('/api/userexist', {"username": 'a'}, format='json')

        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = True  # Explicitly set the return value of 'exists'
        filter.return_value = mock_queryset

        response = user_exist(request)

        assert response.status_code == 409

    @patch('hsabackend.views.user_auth.User.objects.filter')
    def test_user_not_exist(self, filter):
        factory = APIRequestFactory()
        request = factory.post('/api/userexist', {"username": 'a'}, format='json')

        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = False
        filter.return_value = mock_queryset

        response = user_exist(request)
        assert response.status_code == 200
