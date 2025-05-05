from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.job import Job
from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.bookings import create_event


class CreateBookingTest(BaseTestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_bad_date(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.post('api/create/booking')
        request.user = mock_user
        response = create_event(request)

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
            "startTime": "2025-05-25T14:30:00",
            "endTime": "2023-04-25T15:30:00",
            "bookingType": "internal",
            "backColor": "#FF5733",
            "status": "confirmed",
            "jobID": 42
        })
        request.user = mock_user
        response = create_event(request)

        assert response.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.bookings.Job.objects.get')
    def test_job_not_found(self, job, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org
        job.side_effect = Job.DoesNotExist

        factory = APIRequestFactory()
        request = factory.post('api/edit/booking/1', {
            "eventName": "Team Sync",
            "startTime": "2021-05-25T14:30:00",
            "endTime": "2023-04-25T15:30:00",
            "bookingType": "internal",
            "backColor": "#FF5733",
            "status": "confirmed",
            "jobID": 42
        })
        request.user = mock_user
        response = create_event(request)

        assert response.status_code == 400  # this is because the user needs to give valid job id

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.bookings.Job.objects.get')
    @patch('hsabackend.views.bookings.BookingSerializer')
    def test_booking_serializer_invalid(self, booking, job, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mock_booking = Mock()
        booking.return_value = mock_booking
        mock_booking.is_valid.return_value = False

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org
        job.return_value = Job()

        factory = APIRequestFactory()
        request = factory.post('api/edit/booking/1', {
            "eventName": "Team Sync",
            "startTime": "2021-05-25T14:30:00",
            "endTime": "2023-04-25T15:30:00",
            "bookingType": "internal",
            "backColor": "#FF5733",
            "status": "confirmed",
            "jobID": 42
        })
        request.user = mock_user
        response = create_event(request)
        assert response.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.bookings.Job.objects.get')
    @patch('hsabackend.views.bookings.BookingSerializer')
    def test_booking_serializer_valid(self, booking, job, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org
        job.return_value = Job()

        factory = APIRequestFactory()
        request = factory.post('api/edit/booking/1', {
            "eventName": "Team Sync",
            "startTime": "2021-05-25T14:30:00",
            "endTime": "2023-04-25T15:30:00",
            "bookingType": "internal",
            "backColor": "#FF5733",
            "status": "confirmed",
            "jobID": 42
        })
        request.user = mock_user
        response = create_event(request)

        booking.is_valid.return_value = True

        assert response.status_code == 201
