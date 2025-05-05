from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.customer import Customer
from hsabackend.models.job import Job
from hsabackend.models.organization import Organization
from hsabackend.tests import BaseTestCase
from hsabackend.views.jobs import get_job_individual_data, edit_job


class ViewJobTest(BaseTestCase):

    def test_get_job_individual_data_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False

        factory = APIRequestFactory()
        request = factory.get('/api/get/job/1')

        response = get_job_individual_data(request, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_individual_data_job_not_found(self, org, job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        job.return_value = None
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        factory = APIRequestFactory()
        request = factory.get('/api/get/job/1')
        request.user = mock_user

        response = get_job_individual_data(request, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_get_job_individual_data_valid(self, get_org, get_job):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        org = Organization()
        org.pk = 1
        org.is_onboarding = False
        get_org.return_value = org

        mock_response = {
            "id": 1,
            "jobStatus": "",
            "startDate": "",
            "endDate": "",
            "description": "",
            "customerName": "",
            "customerID": 1,
            "requestorAddress": "",
            "requestorCity": "",
            "requestorState": "",
            "requestorZip": ""
        }

        job = Mock(spec=Job)
        job.pk = 1
        job.json.return_value = mock_response
        get_job.return_value = job

        factory = APIRequestFactory()
        request = factory.get('/api/get/job/1')
        request.user = mock_user

        response = get_job_individual_data(request, 1)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"] == mock_response

    def test_edit_job_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False

        factory = APIRequestFactory()
        request = factory.post('/api/edit/job/1')
        request.user = mock_user
        response = edit_job(request, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_job_not_found(self, org, job_name):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        job_name.side_effect = Job.DoesNotExist
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        factory = APIRequestFactory()
        request = factory.post('/api/edit/job/0')
        request.user = mock_user
        response = edit_job(request, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('hsabackend.views.jobs.Customer.objects.get')
    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_job_invalid(self, org, job_name, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_job_name = MagicMock(spec=Job)
        customer.return_value = Customer()
        job_name.return_value = mock_job_name
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        mock_job_name.full_clean.side_effect = ValidationError({'description': ['This field is required.']})

        factory = APIRequestFactory()
        request = factory.post('/api/edit/job/1',
                               data={
                                   "job_status": "created",
                                   "start_date": "2026-01-02",
                                   "end_date": "2026-02-02",
                                   "description": "Test Job",
                                   "city": "Test City",
                                   "state": "Iowa",
                                   "zip": "99999",
                                   "address": "Test Address",
                               })
        request.user = mock_user
        response = edit_job(request, 1)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.jobs.Customer.objects.get')
    @patch('hsabackend.views.jobs.Job.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_job_valid(self, org, job_name, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_job_name = MagicMock(spec=Job)
        customer.return_value = Customer()
        job_name.return_value = mock_job_name
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        factory = APIRequestFactory()
        request = factory.post('/api/edit/job/1',
                               data={
                                   "job_status": "created",
                                   "start_date": "2026-01-02",
                                   "end_date": "2026-02-02",
                                   "description": "Test Job",
                                   "city": "Test City",
                                   "state": "Iowa",
                                   "zip": "99999",
                                   "address": "Test Address",
                               })
        request.user = mock_user
        response = edit_job(request, 1)

        assert response.status_code == status.HTTP_200_OK