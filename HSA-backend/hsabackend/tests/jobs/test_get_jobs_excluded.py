from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.jobs import get_job_excluded_table_data


class GetJobsExcludedTest(BaseTestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def job_excluded_no_pagesize(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/exclude?offset=10')
        request.user = mock_user
        response = get_job_excluded_table_data(request)

        assert response.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def job_excluded_invalid_pagesize(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/exclude?offset=10&pagesize=sss')
        request.user = mock_user
        response = get_job_excluded_table_data(request)

        assert response.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def job_excluded_ok(self, orgg):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        orgg.return_value = org

        factory = APIRequestFactory()
        request = factory.get('/api/get/jobs/exclude?offset=10&pagesize=10')
        request.user = mock_user
        response = get_job_excluded_table_data(request)

        assert response.status_code == 200
