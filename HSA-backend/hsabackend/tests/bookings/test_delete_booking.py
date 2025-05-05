from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.bookings import delete_event


class DeleteBookingTest(BaseTestCase):
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
