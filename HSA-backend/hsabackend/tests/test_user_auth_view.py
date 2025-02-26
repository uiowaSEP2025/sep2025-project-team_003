from rest_framework.test import APITestCase
from unittest.mock import patch
from rest_framework import status
from django.contrib.auth.models import User

class UserAuthViewTest(APITestCase):
    @patch('hsabackend.views.user_auth.authenticate')
    def test_invalid_credentials_should_not_log_in(self, mock_auth):
        mock_auth.return_value = None
        response = self.client.post('/api/login', {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['message'], 'Invalid credentials')

    @patch('hsabackend.views.user_auth.authenticate')
    @patch('hsabackend.views.user_auth.login')
    def test_valid_credentials_should_log_in(self, mock_login, mock_authenticate):
        mock_user = User()
        mock_login.return_value = None
        mock_authenticate.return_value = mock_user

        response = self.client.post('/api/login', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Login successful!')