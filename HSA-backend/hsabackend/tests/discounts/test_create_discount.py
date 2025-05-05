from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.discounts import create_discount


class CreateDiscountTest(BaseTestCase):
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
    def test_create_disount_validation_failed(self, discnt, org):
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
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
    def test_create_disount_create_ok(self, discnt, org):
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        mock_discnt = Mock()

        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        discnt.return_value = mock_discnt

        factory = APIRequestFactory()
        request = factory.post('/api/create/discount', data={
            "name": "starwars",
            "percent": "22.0"
        })
        request.user = mock_user
        response = create_discount(request)

        mock_discnt.save.assert_called_once()
        assert response.status_code == status.HTTP_201_CREATED


