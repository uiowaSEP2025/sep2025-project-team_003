from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from django.db.models import QuerySet, Q
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.jobs import get_job_table_data


class TestGetJobTable(BaseTestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_table_data_invalid(self, get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        get.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs?search')
        request.user = mock_user
        response = get_job_table_data(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_table_data_nonint(self, get):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        get.return_value = org
        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs?pagesize=1&offset=c')
        request.user = mock_user
        response = get_job_table_data(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.jobs.Job.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_table_data_valid_query(self, get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        get.return_value = org
        qs = MagicMock(spec=QuerySet)
        filter.return_value = qs

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs?search=bob&pagesize=10&offset=10')
        request.user = mock_user
        response = get_job_table_data(request)

        assert response.status_code == status.HTTP_200_OK
        qs.filter.assert_called_with(
            Q(customer__first_name__icontains='bob') | Q(customer__last_name__icontains='bob') | Q(
                start_date__icontains='bob') | Q(end_date__icontains='bob') | Q(job_status__icontains='bob') | Q(
                description__icontains='bob'))

    @patch('hsabackend.views.jobs.Job.objects.filter')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_table_data_valid_empty_query(self, get, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.pk = 1
        org.is_onboarding = False
        get.return_value = org
        filter.return_value = MagicMock(spec=QuerySet)

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs?search&pagesize=10&offset=10')
        request.user = mock_user
        response = get_job_table_data(request)

        assert response.status_code == status.HTTP_200_OK
        filter.assert_called_with(organization=1)
