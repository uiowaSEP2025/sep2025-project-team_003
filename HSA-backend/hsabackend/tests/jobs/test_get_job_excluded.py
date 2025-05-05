from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.jobs import get_job_excluded_table_data


class GetJobExcludedTest(BaseTestCase):

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_no_pagesize(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        factory = APIRequestFactory()
        request = factory.get('api/get/jobs/exclude?offset=1')
        request.user = mock_user

        res = get_job_excluded_table_data(request)

        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_bad_pagesize(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        factory = APIRequestFactory()
        request = factory.get('api/get/jobs/exclude?offset=1&pagesize=s')
        request.user = mock_user

        res = get_job_excluded_table_data(request)

        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.jobs.Job.objects.filter')
    def test_ok(self, filter, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mock_org = Organization()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        mock_filter = Mock(name="qs")
        filter.return_value = mock_filter
        exclude = Mock(name="exclude")
        mock_filter.exclude.return_value = exclude
        filter2 = MagicMock(name="filter2")
        exclude.filter.return_value = filter2

        factory = APIRequestFactory()
        request = factory.get('api/get/jobs/exclude?offset=1&pagesize=2')
        request.user = mock_user

        res = get_job_excluded_table_data(request)

        assert res.status_code == 200
