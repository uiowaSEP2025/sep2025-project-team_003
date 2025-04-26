from unittest.mock import patch
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.models.organization import Organization
from hsabackend.views.bookings import get_booking_data, delete_event, edit_event

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
    def test_get_booking_bad_date(self,orgg):
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
    def test_get_booking_bad_contractor_id(self,orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get('api/get/bookings?from=jf&to=jd&contractor=asdasdas')
        request.user = mock_user  
        response = get_booking_data(request)

        assert response.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_bookings_ok(self,orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get('api/get/bookings?from=2023-04-25T14:30:00&to=2023-04-25T14:30:00&contractor=1')
        request.user = mock_user  
        response = get_booking_data(request)

        assert response.status_code == 200
    
class CreateBooking(APITestCase):
    pass

class UpdateBooking(APITestCase):
    
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_bad_date(self,orgg):
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
    def test_start_after_end(self,orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.post('api/edit/booking/1?startTime=2023-04-25T14:30:00&endTime=2022-04-25T14:30:00')
        request.user = mock_user  
        response = edit_event(request, 1)

        assert response.status_code == 400

    def test_job_dosent_exist(self):
        pass

    def test_event_dosent_exist(self):
        pass

    def test_event_serializer_invalid(self):
        pass

    def test_save_ok(self):
        pass


class DeleteBooking(APITestCase):
    @patch('hsabackend.views.bookings.Booking.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_delete_not_found(self,orgg,filter):
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
        response = delete_event(request,1)
        assert response.status_code == 404
        
    @patch('hsabackend.views.bookings.Booking.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_delete_ok(self,orgg,filter):
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
        response = delete_event(request,1)
        assert response.status_code == 404




