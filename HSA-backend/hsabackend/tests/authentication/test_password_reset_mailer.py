import unittest
from unittest.mock import patch, MagicMock

from hsabackend.mailing.password_reset import send_password_reset


class SendPasswordResetTest(unittest.TestCase):

    @patch('hsabackend.mailing.password_reset.get_url')  
    @patch('hsabackend.mailing.password_reset.EmailMultiAlternatives')  
    @patch('os.environ.get')  
    def test_send_password_reset_success(self, mock_get_env, mock_email, mock_get_url):
        # Arrange
        reset_token = 'fake-token'
        username = 'testuser'
        email = 'testuser@example.com'
        mock_get_url.return_value = 'https://example.com'
        mock_get_env.return_value = 'noreply@example.com'  

        mock_email_instance = MagicMock()
        mock_email.return_value = mock_email_instance

        # Act
        send_password_reset(reset_token, username, email)

        mock_get_url.assert_called_once()

        mock_email.assert_called_once()

        mock_email_instance.attach_alternative.assert_called_once()

        mock_email_instance.send.assert_called_once()
