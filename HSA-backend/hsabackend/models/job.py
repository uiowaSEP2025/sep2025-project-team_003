from django.db import models
from . import contractor
from . import organization
from . import material
from . import service
class Job(models.Model):
    """A request for service from a customer to an organization"""
    job_status = models.CharField(max_length=50)
    start_date = models.DateField
    end_date = models.DateField
    description = models.CharField(max_length=200)
    contractor = models.ManyToManyField(contractor.Contractor)
    organization = models.ForeignKey(organization.Organization, on_delete=models.CASCADE)
    materials = models.ManyToManyField(material.Material, through="MaterialJob")
    service = models.ManyToManyField(service.Service)

    def __str__(self):
        return f"<Job, organization: {self.organization}, description: {self.description}>"
    
# this must be here or we get a circular import error
class MaterialJob(models.Model):
    unit_cost = models.FloatField()
    units_used = models.IntegerField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    material = models.ForeignKey(material.Material, on_delete=models.CASCADE)