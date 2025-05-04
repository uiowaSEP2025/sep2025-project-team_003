from unittest.mock import patch
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.models.organization import Organization
from hsabackend.views.bookings import get_booking_data, delete_event, edit_event, create_event
from hsabackend.models.job import Job
from hsabackend.models.booking import Booking

class GetBookingsData(APITestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_booking_no_date(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get('api/get/bookings')
        request.user = mock_user
        response = get_booking_data(request)

        assert response.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_booking_bad_date(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get('api/get/bookings?from=jf&to=jd')
        request.user = mock_user
        response = get_booking_data(request)

        assert response.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_booking_bad_contractor_id(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get(
            'api/get/bookings?from=jf&to=jd&contractor=asdasdas')
        request.user = mock_user
        response = get_booking_data(request)

        assert response.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.bookings.BookingSerializer')
    @patch('hsabackend.views.bookings.Job.objects.get')
    @patch('hsabackend.views.bookings.JobService.objects.filter')
    @patch('hsabackend.views.bookings.JobMaterial.objects.filter')
    @patch('hsabackend.views.bookings.JobContractor.objects.filter')
    def test_get_bookings_ok(self, f, d,c,a,mock_serializer, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mock_s = Mock()
        mock_serializer.return_value = mock_s
        mock_s.data = [{"job": "job"}]


        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get(
            'api/get/bookings?from=2023-04-25T14:30:00&to=2023-04-25T14:30:00&contractor=1')
        request.user = mock_user
        response = get_booking_data(request)

        assert response.status_code == 200

        


class CreateBooking(APITestCase):
    
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

        assert response.status_code == 400 # this is because the user needs to give valid job id

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


class UpdateBooking(APITestCase):

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

class DeleteBooking(APITestCase):
    @patch('hsabackend.views.bookings.Booking.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_delete_not_found(self, orgg, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        mockqs = Mock()
        filter.return_value = mockqs

        mockqs.exists.return_value = False

        factory = APIRequestFactory()
        request = factory.post('/api/delete/booking/1')
        request.user = mock_user
        response = delete_event(request, 1)
        assert response.status_code == 404

    @patch('hsabackend.views.bookings.Booking.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_delete_ok(self, orgg, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        mockqs = Mock()
        filter.return_value = mockqs

        mockqs.exists.return_value = False

        factory = APIRequestFactory()
        request = factory.post('/api/delete/booking/1')
        request.user = mock_user
        response = delete_event(request, 1)
        assert response.status_code == 404
