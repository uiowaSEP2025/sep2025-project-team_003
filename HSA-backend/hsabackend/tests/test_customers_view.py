from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from hsabackend.views.customers import get_customer_excluded_table_data, get_customer_table_data, create_customer, edit_customer, delete_customer
from rest_framework.test import APITestCase
from hsabackend.models.organization import Organization
from django.db.models import QuerySet
from django.db.models import Q
from hsabackend.models.customer import Customer
from django.core.exceptions import ValidationError

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

    def test_get_customer_excluded_table_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/customers/exclude?excludeIDs=1&search=bob&pagesize=5&offset=0')
        request.user = mock_user  
        response = get_customer_excluded_table_data(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_get_customer_excluded_table_data_invalid(self,get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        factory = APIRequestFactory()
        request = factory.get('/api/get/customers/exclude?excludeIDs=1&search')
        request.user = mock_user  
        response = get_customer_excluded_table_data(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.customers.Customer.objects.exclude')
    @patch('hsabackend.views.customers.Customer.objects.filter')
    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_get_customer_excluded_table_data_valid_query(self, get, filter, exclude):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        get.return_value = Organization()
        qs = MagicMock(spec=QuerySet) # needed because it's sliced in the code
        filter.return_value = qs
        exclude.return_value = qs

        factory = APIRequestFactory()
        request = factory.get('/api/get/customers/exclude?excludeIDs=1&search=bob&pagesize=20&offset=0')
        request.user = mock_user  
        response = get_customer_excluded_table_data(request)
        
        assert response.status_code == status.HTTP_200_OK
        qs.exclude.assert_called_with(id__in=[1])
        qs.filter.assert_not_called()

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
        request = factory.get('/api/get/customers/exclude?excludeIDs=1&search=bob&pagesize=5&offset=0')
        request.user = mock_user  
        response = get_customer_excluded_table_data(request)
        
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
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.doe@example.com',
                    'phone': '',
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
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.doe@example.com',
                    'phoneno': '1231231234',
                    'notes': 'Sample note for testing purposes.'
                    })
        request.user = mock_user   
        response = create_customer(request)
        cust_obj.save.assert_called_once()
        assert response.status_code == status.HTTP_201_CREATED

    def test_edit_customer_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/customers/1')
        request.user = mock_user  
        response = edit_customer(request,1)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.customers.Customer.objects.filter')
    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_edit_customer_not_found(self,org, cust):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_cust = MagicMock()
        mock_cust.exists.return_value = False
        cust.return_value = mock_cust
        org.return_value = Organization()
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/customers/1')
        request.user = mock_user  
        response = edit_customer(request, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.customers.Customer.objects.filter')
    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_edit_customer_invalid(self,org, cust):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        cust_qs = MagicMock()
        cust_qs.exists.return_value = True
        cust.return_value = cust_qs
        org.return_value = Organization()
        mock_cust = MagicMock(name="mock cust")
        cust_qs.__getitem__.side_effect = lambda x: mock_cust
        mock_cust.full_clean.side_effect = ValidationError({'first_name': ['This field is required.']})

        factory = APIRequestFactory()
        request = factory.post('/api/edit/customers/1',
                    data={
                        'first_name': 'John',
                        'last_name': 'Doe',
                        'email': 'john.doe@example.com',
                        'phoneno': '1231231234',
                        'notes': 'Sample note for testing purposes.'
                    })
        request.user = mock_user  
        response = edit_customer(request, 1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.customers.Customer.objects.filter')
    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_edit_customer_valid(self,org, cust):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_cust = MagicMock()
        mock_cust.exists.return_value = True
        cust.return_value = mock_cust

        org.return_value = Organization()

        factory = APIRequestFactory()
        request = factory.post('/api/edit/customers/1',
                    data={
                        'first_name': 'John',
                        'last_name': 'Doe',
                        'email': 'john.doe@example.com',
                        'phoneno': '1231231234',
                        'notes': 'Sample note for testing purposes.'
                    })
        request.user = mock_user  
        response = edit_customer(request, 1)
        
        assert response.status_code == status.HTTP_200_OK

    def test_delete_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/customers/1')
        request.user = mock_user  
        response = delete_customer(request,1)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.customers.Customer.objects.filter')
    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_delete_not_found(self, org, cust):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True 
        org.return_value = Organization()
        cust_query_set = MagicMock()
        cust_query_set.exists.return_value = False
        cust.return_value = cust_query_set

        factory = APIRequestFactory()
        request = factory.post('/api/delete/customers/1')
        request.user = mock_user  
        response = delete_customer(request,1)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.customers.Customer.objects.filter')
    @patch('hsabackend.views.customers.Organization.objects.get')
    def test_delete_success(self, org, cust):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True 
        org.return_value = Organization()
        cust_query_set = MagicMock()
        cust_query_set.exists.return_value = True
        cust.return_value = cust_query_set

        factory = APIRequestFactory()
        request = factory.post('/api/delete/customers/1')
        request.user = mock_user  
        response = delete_customer(request,1)
        assert response.status_code == status.HTTP_200_OK