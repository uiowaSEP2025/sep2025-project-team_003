from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.discounts import delete_discount


class DeleteDiscountTest(BaseTestCase):
    def test_delete_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False

        factory = APIRequestFactory()
        request = factory.post('/api/delete/discount/1')
        request.user = mock_user
        response = delete_discount(request, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.discounts.DiscountType.objects.filter')
    @patch('hsabackend.views.discounts.Organization.objects.get')
    def test_delete_not_found(self, org, discnt):
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        discnt_qs = MagicMock()
        discnt.return_value = discnt_qs

        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        discnt_qs.exists.return_value = False

        factory = APIRequestFactory()
        request = factory.post('/api/delete/discount/1')
        request.user = mock_user
        response = delete_discount(request, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.discounts.DiscountType.objects.filter')
    @patch('hsabackend.views.discounts.Organization.objects.get')
    def test_delete_ok(self, org, discnt):
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        discnt_qs = MagicMock()
        discnt.return_value = discnt_qs

        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        discnt_qs.exists.return_value = True
        mock_discnt = Mock()
        discnt_qs.__getitem__.side_effect = lambda x: mock_discnt

        factory = APIRequestFactory()
        request = factory.post('/api/delete/discount/1')
        request.user = mock_user
        response = delete_discount(request, 1)

        mock_discnt.delete.assert_called_once()

        assert response.status_code == status.HTTP_200_OK