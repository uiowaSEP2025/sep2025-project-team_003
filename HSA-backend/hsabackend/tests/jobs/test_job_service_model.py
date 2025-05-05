from django.test import TestCase
from hsabackend.models.service import Service
from hsabackend.models.job import Job, JobsServices
class JobServiceModelTest(TestCase):

    def setUp(self):
        self.service = Service(
            name='Test Service',
            description='This is a test service.',
            default_fee=100,
        )
        self.job = Job()
        
        self.job_service = JobsServices(
            job=self.job,
            service=self.service,
            fee=50
        )

    
    def test_json_method(self):
        expected_json = {
            'id': self.job_service.pk,
            'serviceID': self.service.id,
            'serviceName': self.service.name,
            'serviceDescription': self.service.description
        }
        
        self.assertEqual(self.job_service.json(), expected_json)

    def test_get_service_info_for_detailed_invoice_method(self):
        expected_service_info = {
            "service name": self.service.name,
            "service description": self.service.description,
            "fee": self.job_service.fee
        }
        
        self.assertEqual(self.job_service.get_service_info_for_detailed_invoice(), expected_service_info)
