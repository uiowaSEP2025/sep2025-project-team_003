from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.booking import Booking
from hsabackend.models.job import Job
from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.bookings import edit_event


class UpdateBookingTest(BaseTestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_bad_date(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.post('api/edit/booking/1')
        request.user = mock_user
        response = edit_event(request, 1)

        assert response.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_start_after_end(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.post('api/edit/booking/1', {
            "eventName": "Team Sync",
            "startTime": "2023-05-25T14:30:00",
            "endTime": "2023-04-25T15:30:00",
            "bookingType": "internal",
            "backColor": "#FF5733",
            "status": "confirmed",
            "jobID": 42
        })
        request.user = mock_user
        response = edit_event(request, 1)

        assert response.status_code == 400

    @patch('hsabackend.views.bookings.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_job_dosent_exist(self, orgg, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        job.side_effect = Job.DoesNotExist

        factory = APIRequestFactory()
        request = factory.post('api/edit/booking/1', {
            "eventName": "Team Sync",
            "startTime": "2023-05-25T14:30:00",
            "endTime": "2023-06-25T15:30:00",
            "bookingType": "internal",
            "backColor": "#FF5733",
            "status": "confirmed",
            "jobID": 42
        })
        request.user = mock_user
        response = edit_event(request, 1)

        assert response.status_code == 404

    @patch('hsabackend.views.bookings.Booking.objects.get')
    @patch('hsabackend.views.bookings.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_event_dosent_exist(self, orgg, job, event):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        event.side_effect = Booking.DoesNotExist

        factory = APIRequestFactory()
        request = factory.post('api/edit/booking/1', {
            "eventName": "Team Sync",
            "startTime": "2023-05-25T14:30:00",
            "endTime": "2023-06-25T15:30:00",
            "bookingType": "internal",
            "backColor": "#FF5733",
            "status": "confirmed",
            "jobID": 42
        })
        request.user = mock_user
        response = edit_event(request, 1)

        assert response.status_code == 404

    @patch('hsabackend.views.bookings.BookingSerializer')
    @patch('hsabackend.views.bookings.Booking.objects.get')
    @patch('hsabackend.views.bookings.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_event_serializer_invalid(self, orgg, job, event, serial):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        mock_serial = Mock()
        mock_serial.is_valid.return_value = False
        serial.return_value = mock_serial

        factory = APIRequestFactory()
        request = factory.post('api/edit/booking/1', {
            "eventName": "Team Sync",
            "startTime": "2023-05-25T14:30:00",
            "endTime": "2023-06-25T15:30:00",
            "bookingType": "internal",
            "backColor": "#FF5733",
            "status": "confirmed",
            "jobID": 42
        })
        request.user = mock_user
        response = edit_event(request, 1)

        assert response.status_code == 400

    @patch('hsabackend.views.bookings.BookingSerializer')
    @patch('hsabackend.views.bookings.Booking.objects.get')
    @patch('hsabackend.views.bookings.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_save_ok(self, orgg, job, event, serial):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        mock_serial = Mock()
        mock_serial.is_valid.return_value = True
        serial.return_value = mock_serial

        factory = APIRequestFactory()
        request = factory.post('api/edit/booking/1', {
            "eventName": "Team Sync",
            "startTime": "2023-05-25T14:30:00",
            "endTime": "2023-06-25T15:30:00",
            "bookingType": "internal",
            "backColor": "#FF5733",
            "status": "confirmed",
            "jobID": 42
        })
        request.user = mock_user
        response = edit_event(request, 1)
        mock_serial.save.assert_called_once()

        assert response.status_code == 200
