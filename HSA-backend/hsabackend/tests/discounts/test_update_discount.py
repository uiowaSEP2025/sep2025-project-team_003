from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.discounts import edit_discount


class EditDiscountTest(BaseTestCase):
    def test_edit_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False

        factory = APIRequestFactory()
        request = factory.post('/api/edit/discount/1')
        request.user = mock_user
        response = edit_discount(request, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.discounts.DiscountType.objects.filter')
    @patch('hsabackend.views.discounts.Organization.objects.get')
    def test_edit_not_exist(self, org, discnt):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        discnt_mock = Mock()
        discnt.return_value = discnt_mock
        discnt_mock.exists.return_value = False

        factory = APIRequestFactory()
        request = factory.post('/api/edit/discount/1')
        request.user = mock_user
        response = edit_discount(request, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.discounts.DiscountType.objects.filter')
    @patch('hsabackend.views.discounts.Organization.objects.get')
    def test_edit_fails_validation(self, org, discnt):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        discnt_qs = MagicMock()
        discnt.return_value = discnt_qs
        discnt_qs.exists.return_value = True

        factory = APIRequestFactory()
        request = factory.post('/api/edit/discount/1')
        request.user = mock_user

        mock_discnt = Mock()

        discnt_qs.__getitem__.side_effect = lambda x: mock_discnt
        mock_discnt.full_clean.side_effect = ValidationError({'name': ['This field is required.']})

        response = edit_discount(request, 1)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.discounts.DiscountType.objects.filter')
    @patch('hsabackend.views.discounts.Organization.objects.get')
    def test_edit_ok(self, org, discnt):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        discnt_qs = MagicMock()
        discnt.return_value = discnt_qs
        discnt_qs.exists.return_value = True

        factory = APIRequestFactory()
        request = factory.post('/api/edit/discount/1', data={
            "name": "summer sale",
            "percent": "20.00"
        })
        request.user = mock_user
        response = edit_discount(request, 1)

        mock_discnt = Mock()
        discnt_qs.__getitem__.side_effect = lambda x: mock_discnt

        assert response.status_code == status.HTTP_200_OK

