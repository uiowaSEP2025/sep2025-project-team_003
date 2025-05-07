from unittest import TestCase
from hsabackend.mailing.quotes_mailer import accept_reject_quotes, send_quotes_email, encode
from hsabackend.models.job import Job
from unittest.mock import Mock,patch, MagicMock
from hsabackend.models.customer import Customer

class TestJWTEncode(TestCase):
    @patch("hsabackend.mailing.quotes_mailer.jwt.encode")
    def test_jwt_encode(self, mock_jwt_encode):
        mock_job = Mock(spec=Job)
        encode(mock_job)

        mock_jwt_encode.assert_called_once_with(
            mock_job.jwt_json(),
            "vibecodedAPPS-willgetyouHACKED!!",
            algorithm="HS256"
        )

class TestSendQuote(TestCase):

    @patch("hsabackend.mailing.quotes_mailer.EmailMultiAlternatives")
    @patch("hsabackend.mailing.quotes_mailer.encode", return_value="mocktoken")
    @patch("hsabackend.mailing.quotes_mailer.get_url", return_value="https://example.com")
    @patch("hsabackend.mailing.quotes_mailer.os.environ.get", return_value="noreply@example.com")
    def test_send_quotes_email(self, mock_env, mock_get_url, mock_encode, mock_email_multi):
        msg_mock = MagicMock()
        mock_email_multi.return_value = msg_mock
        c = Customer(first_name="Alex", email="alex@example.com")
        j = Job(pk=123, customer=c, quote_status="pending", quote_s3_link="some_url")
        mock_pdf = Mock()

        to_email = send_quotes_email(j, mock_pdf)

        mock_email_multi.assert_called_once()
        msg_mock.attach_alternative.assert_called_once()
        msg_mock.attach.assert_called_once()
        msg_mock.send.assert_called_once()
        self.assertEqual(to_email, "alex@example.com")
        
class TestAcceptReject(TestCase):

    @patch("hsabackend.mailing.quotes_mailer.EmailMultiAlternatives")
    @patch("hsabackend.mailing.quotes_mailer.get_url", return_value="https://example.com")
    @patch("hsabackend.mailing.quotes_mailer.os.environ.get", return_value="noreply@example.com")
    def test_accept_quote(self, mock_env, mock_get_url, mock_email_multi):
        msg_mock = MagicMock()
        mock_email_multi.return_value = msg_mock
        c = Mock()
        c.first_name = "Alex"
        c.email = "alex@example.com"

        j = Mock()
        j.pk = 123
        j.customer = c
        j.quote_status = "pending"
        j.quote_s3_link = "some_url"

        accept_reject_quotes(j, "accept")

        j.save.assert_called_with(update_fields=['quote_status'])
        self.assertEqual(j.quote_status, "accepted")
        self.assertIsNotNone(j.quote_s3_link)
        msg_mock.send.assert_called_once()

    @patch("hsabackend.mailing.quotes_mailer.EmailMultiAlternatives")
    @patch("hsabackend.mailing.quotes_mailer.get_url", return_value="https://example.com")
    @patch("hsabackend.mailing.quotes_mailer.os.environ.get", return_value="noreply@example.com")
    def test_reject_quote(self, mock_env, mock_get_url, mock_email_multi):
        msg_mock = MagicMock()
        mock_email_multi.return_value = msg_mock
        c = Mock()
        c.first_name = "Alex"
        c.email = "alex@example.com"

        j = Mock()
        j.pk = 123
        j.customer = c
        j.quote_status = "pending"
        j.quote_s3_link = "some_url"

        accept_reject_quotes(j, "reject")
        j.save.assert_called_with(update_fields=['quote_status', 'quote_s3_link'])

        self.assertEqual(j.quote_status, "rejected")
        self.assertIsNone(j.quote_s3_link)
        msg_mock.send.assert_called_once()