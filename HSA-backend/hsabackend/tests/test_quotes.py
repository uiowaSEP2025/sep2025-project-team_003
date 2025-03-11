from unittest.mock import MagicMock, Mock
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

class testQuotesView(APITestCase):
    def test_get_quotes_by_cust_id_unauth(self):
        pass

    def test_get_quotes_by_cust_id_missing_pagesize(self):
        pass

    def test_get_quotes_by_cust_id_invalid_page_size(self):
        pass

    def test_get_quotes_by_cust_id_ok(self):
        pass