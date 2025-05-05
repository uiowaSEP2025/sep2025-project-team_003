from unittest.mock import patch, Mock

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.bookings import get_booking_data


class GetBookingsDataTest(BaseTestCase):

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
    def test_get_bookings_ok(self, mock_serializer, orgg):
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
            'api/get/bookings?from=2025-04-25T14:30:00&to=2025-05-02T14:30:00&contractor=1')
        request.user = mock_user
        response = get_booking_data(request)

        assert response.status_code == 200