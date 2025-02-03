from django.db import models
from contractor import Contractor
from organization import Organization
from material import Material
from material_job import MaterialJob
from service import Service

class Job(models.Model):
    """A request for service from a customer to an organization"""
    job_status = models.CharField(max_length=50)
    start_date = models.DateField
    end_date = models.DateField
    description = models.CharField(max_length=200)
    contractor = models.ManyToManyField(Contractor)
    organization = models.ManyToOneRel(Organization)
    materials = models.ManyToManyField(Material, through=MaterialJob)
    service = models.ManyToManyField(Service)

    def __str__(self):
        return f"<Job, organization: {self.organization}, customer: {self.customer}, description: {self.description}>"
    