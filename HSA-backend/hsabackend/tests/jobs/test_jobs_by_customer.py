from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.jobs import get_jobs_by_contractor


class JobsByCustomer(BaseTestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_no_pagesize(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/by-contractor?offset=2&contractor=2')
        request.user = mock_user
        response = get_jobs_by_contractor(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_by_contractor_invalid_contractor(self ,orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/by-contractor?offset=2&pagesize=10&contractor=ajajaj')
        request.user = mock_user
        response = get_jobs_by_contractor(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_fetch_ok(self ,orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/by-contractor?offset=2&contractor=2&pagesize=10')
        request.user = mock_user
        response = get_jobs_by_contractor(request)
        assert response.status_code == status.HTTP_200_OK
