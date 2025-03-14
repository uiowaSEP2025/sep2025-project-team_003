from django.db import models
from hsabackend.models.contractor import Contractor
from hsabackend.models.organization import Organization
from hsabackend.models.material import Material
from hsabackend.models.service import Service
from hsabackend.models.model_validators import isNonEmpty, validate_state
from hsabackend.models.customer import Customer

class Job(models.Model):
    """A request for service from a customer to an organization"""
    status_choices = [
        ('created', 'created'),
        ('completed', 'completed'),
    ]


    job_status = models.CharField(max_length=50, choices=status_choices, default="created")
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.CharField(max_length=200, blank=True)
    contractor = models.ManyToManyField(Contractor)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    materials = models.ManyToManyField(Material, through="MaterialJob")
    service = models.ManyToManyField(Service)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    requestor_city = models.CharField(max_length=50,validators=[isNonEmpty])
    requestor_state = models.CharField(max_length=50,validators=[isNonEmpty,validate_state])
    requestor_zip = models.CharField(max_length=10,validators=[isNonEmpty])
    requestor_address = models.CharField(max_length=100,validators=[isNonEmpty])

    def __str__(self):
        return f"<Job, organization: {self.organization}, description: {self.description}>"
    
# this must be here or we get a circular import error
class MaterialJob(models.Model):
    unit_cost = models.DecimalField(max_digits=9, decimal_places=2)
    units_used = models.IntegerField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)