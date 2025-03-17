from django.db import models
from hsabackend.models.contractor import Contractor
from hsabackend.models.job import Job

class JobContractor(models.Model):
    """A preset template that can be used by other entities to create a join entity"""
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)

    def __str__(self):
        return f"<JobsContractors, id:{self.pk}>"
    
    def json(self):
        return {
            'id': self.pk,
            'job_id': self.job.id,
            'contractor_id': self.contractor.id,
        }