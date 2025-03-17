from django.db import models
from hsabackend.models.service import Service
from hsabackend.models.job import Job

class JobService(models.Model):
    """A preset template that can be used by other entities to create a join entity"""
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"<JobsServices, id:{self.pk}>"
    
    def json(self):
        return {
            'id': self.pk,
            'job_id': self.job.id,
            'service_id': self.service.id,
        }