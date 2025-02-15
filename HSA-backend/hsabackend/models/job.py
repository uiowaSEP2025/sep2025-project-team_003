from django.db import models
from hsabackend.models.contractor import Contractor
from hsabackend.models.organization import Organization
from hsabackend.models.material import Material
from hsabackend.models.service import Service

class Job(models.Model):
    """A request for service from a customer to an organization"""
    status_choices = [
        ('created', 'created'),
        ('completed', 'completed'),
    ]


    job_status = models.CharField(max_length=50, choices=status_choices, default="created")
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=200)
    contractor = models.ManyToManyField(Contractor)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    materials = models.ManyToManyField(Material, through="MaterialJob")
    service = models.ManyToManyField(Service)

    def __str__(self):
        return f"<Job, organization: {self.organization}, description: {self.description}>"
    
# this must be here or we get a circular import error
class MaterialJob(models.Model):
    unit_cost = models.FloatField()
    units_used = models.IntegerField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)