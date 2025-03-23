from django.db import models
from hsabackend.models.service import Service
from hsabackend.models.job import Job

class JobService(models.Model):
    """Job service join"""
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"<JobsServices, id:{self.pk}, jobid: {self.job.pk}, serviceid: {self.service.pk}>"
    
    def json(self):
        return {
            'id': self.pk,
            'job_id': self.job.id,
            'service_id': self.service.id,
            'service_name': self.service.service_name
        }
    
    def get_service_info_for_detailed_invoice(self):
        return {
            "service name": self.service.service_name,
            "service description": self.service.service_description
        }