from rest_framework.test import APITestCase
from unittest.mock import Mock, patch, MagicMock
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

from hsabackend.tests import BaseTestCase
from hsabackend.views.invoices import get_invoices, create_invoice, update_invoice, delete_invoice, get_data_for_invoice
from rest_framework import status
from django.core.exceptions import ValidationError
from hsabackend.models.organization import Organization

class InvoiceViewTest(BaseTestCase):
    def test_get_invoice_table_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search&pagesize=100&offset=0')
        request.user = mock_user  
        response = get_invoices(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_get_invoice_table_no_pagesize(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search&&offset=0')
        request.user = mock_user  
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        response = get_invoices(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_get_invoice_table_pagesize_string(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search&&offset=0&pagesize=ae')
        request.user = mock_user  
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        response = get_invoices(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    @patch('hsabackend.views.invoices.Invoice.objects.select_related')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_get_invoice_table_ok(self, org, invoice):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/materials?search&&offset=0&pagesize=2')
        request.user = mock_user  
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        mock_select = Mock()
        invoice.return_value = mock_select
        mock_filtered = MagicMock()
        mock_select.filter.return_value = mock_filtered

        response = get_invoices(request)
        
        assert response.status_code == status.HTTP_200_OK

    def test_create_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('api/create/invoice')
        request.user = mock_user  
        response = create_invoice(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_create_customer_isnt_int(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.post('api/create/invoice', {
            "customerID": "1",
            "quoteIDs": []
        }, format='json')
        request.user = mock_user  
        response = create_invoice(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_create_quotes_isnt_list(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.post('api/create/invoice', {
            "customerID": 1,
            "quoteIDs": ""
        }, format='json')
        request.user = mock_user  
        response = create_invoice(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_create_quotes_is_empty(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.post('api/create/invoice', {
            "customerID": 1,
            "quoteIDs": []
        }, format='json')
        request.user = mock_user  
        response = create_invoice(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_create_bad_status(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.post('api/create/invoice', {
            "customerID": 1,
            "quoteIDs": [1],
            "status": "bad",
            "issuedDate": "bad",
            "dueDate": "bad"
        }, format='json')
        request.user = mock_user  
        response = create_invoice(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_create_invalid_date(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.post('api/create/invoice', {
            "customerID": 1,
            "quoteIDs": [1],
            "status": "issued",
            "issuedDate": "bad",
            "dueDate": "bad"
        }, format='json')
        request.user = mock_user  
        response = create_invoice(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_due_before_issued(self):
        pass

    @patch('hsabackend.views.invoices.Customer.objects.filter')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_create_customer_dosent_exist(self, org, get_cust):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        cust_qs = MagicMock()
        cust_qs.exists.return_value = False
        get_cust.return_value = cust_qs

        factory = APIRequestFactory()
        request = factory.post('api/create/invoice', {
            "customerID": 1,
            "quoteIDs": [1],
            "status": "created",
            "tax": "0.06"
        }, format='json')
        request.user = mock_user  
        response = create_invoice(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.invoices.Invoice')
    @patch('hsabackend.views.invoices.Customer.objects.filter')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_create_invoice_validation_fail(self, org, get_cust, invoice):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        cust_qs = MagicMock()
        cust_qs.exists.return_value = True
        get_cust.return_value = cust_qs

        cust_mock = Mock()
        cust_qs.__getitem__.side_effect = lambda x: cust_mock

        mock_invoice = Mock()
        invoice.return_value = mock_invoice
        mock_invoice.full_clean.side_effect = ValidationError({'firstn': ['This field is required.']})

        factory = APIRequestFactory()
        request = factory.post('api/create/invoice', {
            "customerID": 1,
            "quoteIDs": [1],
            "status": "created",
            "tax": "0.06"
        }, format='json')
        request.user = mock_user  
        response = create_invoice(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Quote.objects.filter')
    @patch('hsabackend.views.invoices.Invoice')
    @patch('hsabackend.views.invoices.Customer.objects.filter')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_create_invoice_success(self, org, get_cust, invoice, quote_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        cust_qs = MagicMock()
        cust_qs.exists.return_value = True
        get_cust.return_value = cust_qs

        cust_mock = Mock()
        cust_qs.__getitem__.side_effect = lambda x: cust_mock

        mock_invoice = Mock()
        invoice.return_value = mock_invoice
        
        mock_quote_qs = Mock()
        quote_filter.return_value = mock_quote_qs

        factory = APIRequestFactory()
        request = factory.post('api/create/invoice', {
            "customerID": 1,
            "quoteIDs": [1],
            "status": "created",
            "tax": "0.06"
        }, format='json')
        request.user = mock_user  
        response = create_invoice(request)

        mock_quote_qs.update.assert_called_with(invoice=mock_invoice)
        mock_invoice.save.assert_called_once()

        assert response.status_code == status.HTTP_201_CREATED

    def test_update_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/invoice/1')
        request.user = mock_user  
        response = update_invoice(request,1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_update_quotes_not_list(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/invoice/1', {
            "quoteIDs": '[1]'
        }, format='json')
        request.user = mock_user  
        response = update_invoice(request,1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_update_quotes_empty(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/invoice/1', {
            "quoteIDs": []
        }, format='json')
        request.user = mock_user  
        response = update_invoice(request,1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_update_invalid_status(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/invoice/1', {
            "quoteIDs": [1],
            "status": "bob"
        }, format='json')
        request.user = mock_user  
        response = update_invoice(request,1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_update_missing_dates(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/invoice/1', {
            "quoteIDs": [1],
            "status": "paid"
        }, format='json')
        request.user = mock_user  
        response = update_invoice(request,1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_update_invalid_date_format(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/invoice/1', {
            "quoteIDs": [1],
            "status": "paid",
            "issuedDate": "peter",
            "dueDate": "dueDate"
        }, format='json')
        request.user = mock_user  
        response = update_invoice(request,1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_update_due_before_issued(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/invoice/1', {
            "quoteIDs": [1],
            "status": "paid",
            "issuedDate": "2005-03-20",
            "dueDate": "2003-03-20"
        }, format='json')
        request.user = mock_user  
        response = update_invoice(request,1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Invoice.objects.filter')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_update_invoice_not_exist(self, org, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        invoice_qs = Mock()
        filter.return_value = invoice_qs
        invoice_qs.exists.return_value = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/invoice/1', {
            "quoteIDs": [1],
            "status": "paid",
            "issuedDate": "2001-03-20",
            "dueDate": "2003-03-20"
        }, format='json')
        request.user = mock_user  
        response = update_invoice(request,1)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.invoices.Quote.objects.exclude')
    @patch('hsabackend.views.invoices.Quote.objects.filter')
    @patch('hsabackend.views.invoices.Invoice.objects.filter')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_update_invoice_fails_validation(self, org, filter, quote, quote_exlude):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        invoice_qs = MagicMock()
        filter.return_value = invoice_qs
        invoice_mock = Mock(name='invoicemock')
        invoice_qs.__getitem__.side_effect = lambda x: invoice_mock
        invoice_mock.status = 'created'
        invoice_mock.full_clean.side_effect = ValidationError({'firstn': ['This field is required.']})
        quote_qs = Mock()
        quote.return_value = quote_qs
        quote_exlude.return_value = quote_qs
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/invoice/1', {
            "quoteIDs": [1],
            "status": "paid",
            "issuedDate": "2001-03-20",
            "dueDate": "2003-03-20"
        }, format='json')
        request.user = mock_user  
        response = update_invoice(request,1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.invoices.Quote.objects.exclude')
    @patch('hsabackend.views.invoices.Quote.objects.filter')
    @patch('hsabackend.views.invoices.Invoice.objects.filter')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_update_invoice_ok_not_created(self, org, filter, quote, quote_exlude):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        invoice_qs = MagicMock()
        filter.return_value = invoice_qs
        invoice_mock = Mock(name='invoicemock')
        invoice_qs.__getitem__.side_effect = lambda x: invoice_mock
        invoice_mock.status = 'created'
        quote_qs = Mock()
        quote.return_value = quote_qs
        quote_exlude.return_value = quote_qs
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/invoice/1', {
            "quoteIDs": [1],
            "status": "paid",
            "issuedDate": "2001-03-20",
            "dueDate": "2003-03-20"
        }, format='json')
        request.user = mock_user  
        response = update_invoice(request,1)
        
        assert response.status_code == status.HTTP_200_OK

    @patch('hsabackend.views.invoices.Quote.objects.exclude')
    @patch('hsabackend.views.invoices.Quote.objects.filter')
    @patch('hsabackend.views.invoices.Invoice.objects.filter')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_update_invoice_ok_created(self, org, filter, quote, quote_exlude):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        
        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        invoice_qs = MagicMock()
        filter.return_value = invoice_qs
        invoice_mock = Mock(name='invoicemock')
        invoice_qs.__getitem__.side_effect = lambda x: invoice_mock
        invoice_mock.status = 'created'
        quote_qs = Mock()
        quote.return_value = quote_qs
        quote_exlude.return_value = quote_qs
        
        factory = APIRequestFactory()
        request = factory.post('/api/edit/invoice/1', {
            "quoteIDs": [1],
            "status": "created"
        }, format='json')
        request.user = mock_user  
        response = update_invoice(request,1)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_delete_not_found(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.post('/api/delete/invoice/1')
        request.user = mock_user  
        response = update_invoice(request,1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.invoices.Invoice.objects.filter')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_delete_unauth(self, org, invoice_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        mock_invoice_qs = Mock()
        invoice_filter.return_value = mock_invoice_qs
        mock_invoice_qs.exists.return_value = False
        
        factory = APIRequestFactory()
        request = factory.post('api/delete/invoice/1')
        request.user = mock_user  
        response = delete_invoice(request,1)

        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    @patch('hsabackend.views.invoices.Invoice.objects.filter')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_delete_ok(self, org, invoice_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        mock_invoice_qs = MagicMock()
        invoice_filter.return_value = mock_invoice_qs
        mock_invoice_qs.exists.return_value = True
        
        invoice_mock = Mock()
        mock_invoice_qs.__getitem__.side_effect = lambda x: invoice_mock
        
        factory = APIRequestFactory()
        request = factory.post('api/delete/invoice/1')
        request.user = mock_user  
        response = delete_invoice(request,1)

        assert response.status_code == status.HTTP_200_OK
        invoice_mock.delete.assert_called_once()


    def test_get_generic_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/invoice/displaydata/1')
        request.user = mock_user  
        response = get_data_for_invoice(request,1)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.invoices.Invoice.objects.filter')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_get_generic_data_not_found(self, org, invoice_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        mock_invoice_qs = Mock()
        mock_invoice_qs.exists.return_value = False
        invoice_filter.return_value = mock_invoice_qs
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/invoice/displaydata/1')
        request.user = mock_user  
        response = get_data_for_invoice(request,1)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.invoices.Quote.objects.filter')
    @patch('hsabackend.views.invoices.Invoice.objects.filter')
    @patch('hsabackend.views.invoices.Organization.objects.get')
    def test_get_generic_data_ok(self, org, invoice_filter, quote_filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        mock_invoice_qs = MagicMock()
        mock_invoice_qs.rexists.return_value = True

        mock_invoice = MagicMock()
        mock_invoice_qs.__getitem__.side_effect = lambda x: mock_invoice
        invoice_filter.return_value = mock_invoice_qs

        mock_quote_qs = MagicMock(name='mock_quote_qs')
        mock_quote_qs.__len__.return_value = 5

        quote_filter.return_value = mock_quote_qs
        
        factory = APIRequestFactory()
        request = factory.get('/api/get/invoice/displaydata/1')
        request.user = mock_user  
        response = get_data_for_invoice(request,1)
        
        assert response.status_code == status.HTTP_200_OK
