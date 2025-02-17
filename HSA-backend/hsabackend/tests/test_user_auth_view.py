from rest_framework.test import APITestCase
from unittest.mock import patch
from rest_framework import status
from django.contrib.auth.models import User

class UserAuthViewTest(APITestCase):

    @patch('hsabackend.views.user_auth.authenticate')
    def test_invalid_credentials_should_not_log_in(self, mock_auth):
        # Mock the authenticate method to return None for invalid credentials
        mock_auth.return_value = None
        
        # Send a POST request with incorrect credentials
        response = self.client.post('/api/login', {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        
        # Assert that the response status is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['message'], 'Invalid credentials')

    @patch('hsabackend.views.user_auth.authenticate')
    @patch('hsabackend.views.user_auth.login')
    def test_valid_credentials_should_log_in(self, mock_login, mock_authenticate):
        # Mock the authenticate method to return a mock user for valid credentials
        mock_user = User()  # This can be any object, it's just used to simulate a successful authentication
        mock_login.return_value = None
        mock_authenticate.return_value = mock_user

        # Send a POST request with correct credentials
        response = self.client.post('/api/login', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        print(f"Mock Authenticate Calls: {mock_authenticate.mock_calls}")

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Login successful!')