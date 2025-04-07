from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from hsabackend.models.organization import Organization
from django.core.exceptions import ValidationError
from hsabackend.views.discounts import get_discounts, create_discount, edit_discount, delete_discount

class DiscountTableTest(APITestCase):
    def test_get_discount_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/discounts?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = get_discounts(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.discounts.Organization.objects.get')
    def test_get_discount_table_data_missing_data(self, org):
        mock_user = Mock(spec=User)
        org.return_value = Organization()
        mock_user.is_authenticated = True
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/discounts?search&offset=0')
        request.user = mock_user  
        response = get_discounts(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.discounts.Organization.objects.get')
    def test_get_discount_table_data_bad_data(self,org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/discounts?search&pagesize=oops&offset=0')
        request.user = mock_user  
        response = get_discounts(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.discounts.DiscountType.objects.filter')
    @patch('hsabackend.views.discounts.Organization.objects.get')
    def test_get_discount_table_data_bad_data(self,org,discounts):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        qs = MagicMock()
        count_qs = MagicMock(name="count_qs")
        qs.filter.return_value = count_qs
        org.return_value = Organization()
        discounts.return_value = qs
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/discounts?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = get_discounts(request)
        count_qs.count.assert_called_once()
        assert response.status_code == status.HTTP_200_OK


class CreateDiscountTest(APITestCase):
    def test_create_disount_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/create/discount')
        request.user = mock_user  
        response = create_discount(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @patch('hsabackend.views.discounts.Organization.objects.get')
    @patch('hsabackend.views.discounts.DiscountType')
    def test_create_disount_validation_failed(self,discnt, org):
        org.return_value = Organization()
        mock_discnt = Mock()
        mock_discnt.full_clean.side_effect = ValidationError({'name': ['This field is required.']})
        discnt.return_value = mock_discnt
        
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        factory = APIRequestFactory()
        request = factory.post('/api/create/discount')
        request.user = mock_user  
        response = create_discount(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.discounts.Organization.objects.get')
    @patch('hsabackend.views.discounts.DiscountType')
    def test_create_disount_create_ok(self,discnt, org):
        org.return_value = Organization()
        mock_discnt = Mock()

        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        discnt.return_value = mock_discnt
        
        factory = APIRequestFactory()
        request = factory.post('/api/create/discount', data={
            "name": "starwars",
            "percent":  "22.0"
        })
        request.user = mock_user  
        response = create_discount(request)
        
        mock_discnt.save.assert_called_once()
        assert response.status_code == status.HTTP_201_CREATED

    

class EditDiscountTest(APITestCase):
    pass

class DeleteDiscountTest(APITestCase):
    pass