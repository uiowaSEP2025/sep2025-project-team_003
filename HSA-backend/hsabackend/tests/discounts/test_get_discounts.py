from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.discounts import get_discounts


class GetDiscountsTest(BaseTestCase):
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
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        mock_user.is_authenticated = True

        factory = APIRequestFactory()
        request = factory.get('/api/get/discounts?search&offset=0')
        request.user = mock_user
        response = get_discounts(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.discounts.Organization.objects.get')
    def test_get_discount_table_data_bad_data(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        factory = APIRequestFactory()
        request = factory.get('/api/get/discounts?search&pagesize=oops&offset=0')
        request.user = mock_user
        response = get_discounts(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.discounts.DiscountType.objects.filter')
    @patch('hsabackend.views.discounts.Organization.objects.get')
    def test_get_discount_table_data_bad_data(self, org, discounts):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        qs = MagicMock()
        count_qs = MagicMock(name="count_qs")
        qs.filter.return_value = count_qs
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        discounts.return_value = qs

        factory = APIRequestFactory()
        request = factory.get('/api/get/discounts?search&pagesize=100&offset=0')
        request.user = mock_user
        response = get_discounts(request)
        count_qs.count.assert_called_once()
        assert response.status_code == status.HTTP_200_OK

