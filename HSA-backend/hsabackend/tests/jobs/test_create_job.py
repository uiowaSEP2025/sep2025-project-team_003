from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from hsabackend.models.contractor import Contractor
from hsabackend.models.customer import Customer
from hsabackend.models.job import Job, JobsServices, JobsMaterials
from hsabackend.models.material import Material
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.tests import BaseTestCase
from hsabackend.views.jobs import create_job


class CreateJobTest(BaseTestCase):
    def test_create_job_unauth(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False

        factory = APIRequestFactory()
        request = factory.post('api/create/job')
        request.user = mock_user
        response = create_job(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.jobs.Customer.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_create_job_auth_invalid(self, org, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        customer.return_value = Customer()
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization

        factory = APIRequestFactory()
        request = factory.post('api/create/job',
                               data={
                                   "jobStatus": "created",
                                   "startDate": "2026-01-02",
                                   "endDate": "2026-02-02",
                                   "description": "Test Job",
                                   "customerID": 1,
                                   "city": "Test City",
                                   "state": "Iowa",
                                   "zip": "99999",
                                   "address": "Test Address",
                                   "contractors": [
                                       {
                                           "id": 2
                                       },
                                       {
                                           "id": 4
                                       }
                                   ],
                                   "services": [
                                       {
                                           "id": 2
                                       }
                                   ],
                                   "materials": [
                                       {
                                           "id": 2,
                                           "unitsUsed": 0,
                                           "pricePerUnit": 0.00
                                       },
                                       {
                                           "id": 4,
                                           "unitsUsed": 0,
                                           "pricePerUnit": 0.00
                                       }
                                   ]
                               })
        request.user = mock_user
        response = create_job(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('hsabackend.views.jobs.Customer.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.jobs.Service.objects.get')
    @patch('hsabackend.views.jobs.Material.objects.get')
    @patch('hsabackend.views.jobs.Contractor.objects.get')
    @patch('hsabackend.views.jobs.Job')
    @patch('hsabackend.views.jobs.JobService')
    @patch('hsabackend.views.jobs.JobMaterial')
    @patch('hsabackend.views.jobs.JobContractor')
    def test_calls_save_if_valid(self, job_contractor, job_material, job_service, job_name, contractor, material,
                                 service, org, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        customer.return_value = Customer()
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        service.return_value = Service()
        material.return_value = Material()
        contractor.return_value = Contractor()

        job_name_obj = MagicMock(spec=Job)
        job_name.return_value = job_name_obj

        job_service_obj = MagicMock(spec=JobsServices)
        job_service.return_value = job_service_obj

        job_material_obj = MagicMock(spec=JobsMaterials)
        job_material.return_value = job_material_obj

        factory = APIRequestFactory()

        mock_data = {
            "jobStatus": "created",
            "startDate": "2026-01-02",
            "endDate": "2026-02-02",
            "description": "Test Job",
            "customerID": 1,
            "city": "Test City",
            "state": "Iowa",
            "zip": "99999",
            "address": "Test Address",
            "contractors": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ],
            "services": [
                {
                    "id": 2
                }
            ],
            "materials": [
                {
                    "id": 2,
                    "unitsUsed": 0,
                    "pricePerUnit": 0.00
                },
                {
                    "id": 4,
                    "unitsUsed": 0,
                    "pricePerUnit": 0.00
                }
            ]
        }

        request = factory.post('api/create/job', data=mock_data, format='json')
        request.user = mock_user
        response = create_job(request)

        job_name_obj.save.assert_called_once()

        assert job_service_obj.save.call_count == len(mock_data["services"])
        assert job_material_obj.save.call_count == len(mock_data["materials"])


        assert response.status_code == status.HTTP_201_CREATED

    @patch('hsabackend.views.jobs.Customer.objects.get')
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.jobs.Service.objects.get')
    @patch('hsabackend.views.jobs.Material.objects.get')
    @patch('hsabackend.views.jobs.Contractor.objects.get')
    @patch('hsabackend.views.jobs.Job')
    @patch('hsabackend.views.jobs.JobService')
    @patch('hsabackend.views.jobs.JobMaterial')
    @patch('hsabackend.views.jobs.JobContractor')
    def test_validation_error(self, job_contractor, job_material, job_service, job_name, contractor, material, service,
                              org, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        customer.return_value = Customer()
        organization = Organization()
        organization.is_onboarding = False
        org.return_value = organization
        service.return_value = Service()
        material.return_value = Material()
        contractor.return_value = Contractor()

        job_name_obj = MagicMock(spec=Job)
        job_name_obj.full_clean.side_effect = ValidationError({'name': ['This field is required.']})
        job_name.return_value = job_name_obj

        job_service_obj = MagicMock(spec=JobsServices)
        job_service.return_value = job_service_obj

        job_material_obj = MagicMock(spec=JobsMaterials)
        job_material.return_value = job_material_obj

        factory = APIRequestFactory()

        mock_data = {
            "jobStatus": "created",
            "startDate": "2026-01-02",
            "endDate": "2026-02-02",
            "description": "Test Job",
            "customerID": 1,
            "city": "Test City",
            "state": "Iowa",
            "zip": "99999",
            "address": "Test Address",
            "contractors": [
                {
                    "id": 2
                },
                {
                    "id": 4
                }
            ],
            "services": [
                {
                    "id": 2
                }
            ],
            "materials": [
                {
                    "id": 2,
                    "unitsUsed": 0,
                    "pricePerUnit": 0.00
                },
                {
                    "id": 4,
                    "unitsUsed": 0,
                    "pricePerUnit": 0.00
                }
            ]
        }

        request = factory.post('api/create/job', data=mock_data, format='json')
        request.user = mock_user
        response = create_job(request)

        assert response.status_code == 400
