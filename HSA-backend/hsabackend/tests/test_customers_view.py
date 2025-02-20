from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.views.customers import get_customer_table_data, create_customer
from rest_framework.test import APITestCase
from hsabackend.models.organization import Organization
from django.db.models import QuerySet
from django.db.models import Q
from hsabackend.models.customer import Customer

class CustomerViewTest(APITestCase):
    def test_get_customer_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/customers?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = get_customer_table_data(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_get_customer_table_data_invalid(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        factory = APIRequestFactory()
        request = factory.get('/api/get/customers?search')
        request.user = mock_user  
        response = get_customer_table_data(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.customers.Customer.objects.filter')
    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_get_customer_table_data_valid_query(self,get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        qs = MagicMock(spec=QuerySet) # needed because it's sliced in the code
        filter.return_value = qs
        

        factory = APIRequestFactory()
        request = factory.get('/api/get/customers?search=bob&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_customer_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        qs.filter.assert_called_with(Q(first_name__icontains='bob') | Q(last_name__icontains='bob') ) 

    @patch('hsabackend.views.customers.Customer.objects.filter')
    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_get_customer_table_data_valid_empty_query(self,get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        org = Mock(spec=Organization)
        org.pk = 1
        get.return_value = org
        filter.return_value = MagicMock(spec=QuerySet)
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/customers?search&pagesize=10&offset=10')
        request.user = mock_user  
        response = get_customer_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        filter.assert_called_with(organization=1) 

    def test_create_customer_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('api/create/customer')
        request.user = mock_user  
        response = create_customer(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_create_customer_auth_invalid(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        
        factory = APIRequestFactory()
        request = factory.post('api/create/customer',
                data={
                    'firstn': 'John',
                    'lastn': 'Doe',
                    'email': 'john.doe@example.com',
                    'phoneno': '',
                    'notes': 'Sample note for testing purposes.'
                    })
        request.user = mock_user  
        response = create_customer(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.customers.Organization.objects.get')
    @patch('hsabackend.views.customers.Customer')
    def test_calls_save_if_valid(self, cust, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org.return_value = Organization()
        cust_obj = MagicMock(spec=Customer)
        cust.return_value = cust_obj
        
        factory = APIRequestFactory()
        request = factory.post('api/create/customer',
                data={
                    'firstn': 'John',
                    'lastn': 'Doe',
                    'email': 'john.doe@example.com',
                    'phoneno': '1231231234',
                    'notes': 'Sample note for testing purposes.'
                    })
        request.user = mock_user   
        response = create_customer(request)
        cust_obj.save.assert_called_once()
        assert response.status_code == status.HTTP_201_CREATED