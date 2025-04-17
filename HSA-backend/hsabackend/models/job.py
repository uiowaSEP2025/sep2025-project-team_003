from django.core.serializers import serialize
from django.db import models
from hsabackend.models.contractor import Contractor
from hsabackend.models.customer import Customer
from hsabackend.models.invoice import Invoice
from hsabackend.models.material import Material
from hsabackend.models.model_validators import isNonEmpty, validate_state
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service


class Job(models.Model):
    """A request for service from a customer to an organization"""
    status_choices = [
        ('created', 'created'),
        ('in-progress', 'in-progress'),
        ('completed', 'completed'),
    ]

    job_status = models.CharField(max_length=50, choices=status_choices, default="created")
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.CharField(max_length=200, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, blank=True, through='JobsServices')
    materials = models.ManyToManyField(Material, blank=True, through='JobsMaterials')
    contractors = models.ManyToManyField(Contractor, blank=True)
    job_city = models.CharField(max_length=50, validators=[isNonEmpty])
    job_state = models.CharField(max_length=50, validators=[isNonEmpty, validate_state])
    job_zip = models.CharField(max_length=10, validators=[isNonEmpty])
    job_address = models.CharField(max_length=100, validators=[isNonEmpty])

    def __str__(self):
        return f"<Job, organization: {self.organization}, description: {self.description}>"
    

    def json(self):
        services_list = serialize('json', self.services.all())
        contractors_list = serialize('json', self.contractors.all())
        materials_list = serialize('json', self.materials.all())

        return {
            'id': self.pk,
            'jobStatus': self.job_status,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'description': self.description,
            'customer': self.customer.json(),
            'materials': materials_list,
            'services': services_list,
            'contractors': contractors_list,
            'jobCity': self.job_city,
            'jobState': self.job_state,
            'jobZip': self.job_zip,
            'jobAddress': self.job_address,
            'invoice': self.invoice,
        }
    
    def json_simplify(self):
        return {
            'id': self.pk,
            # cap at 50 so the table doesn't stretch
        
            'description': self.description[:50] + ("..." if len(self.description) > 50 else ""),
            'job_status': self.job_status,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'customer_name': self.customer.first_name + " " + self.customer.last_name,
        }


class JobsMaterials(models.Model):
    """Join relation for Jobs to Materials with custom fields"""

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=10)
    class Meta:
        db_table = 'hsabackend_job_materials'

    def __str__(self):
        return (f"<Job, Material, Quantity, Price:"
                f" Job: {self.job},"
                f" Material: {self.material},"
                f" Quantity: {self.quantity},"
                f" Unit-Price: {self.unit_price}")

    def json(self):
        return {
            'id': self.pk,
            'job': self.job.id,
            'material': self.material.id,
            'quantity': self.quantity,
            'unit_price': self.unit_price,

        }

    def json_simplify(self):
        return {
            'id': self.pk,
            'job': self.job.id,
            'material': self.material.id,
        }

class JobsServices(models.Model):
    """Join relation for Jobs to Services with custom fields"""

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    minutes = models.IntegerField()
    hourly_rate = models.DecimalField(decimal_places=2, max_digits=10)
    class Meta:
        db_table = 'hsabackend_job_services'

    def __str__(self):
        return (f"<Job, Service, Minutes, Rate:"
                f" Job: {self.job},"
                f" Service: {self.service},"
                f" Minutes: {self.minutes},"
                f" Hourly Rate: {self.hourly_rate}")

    def json(self):
        return {
            'id': self.pk,
            'job': self.job.id,
            'service': self.service.id,
            'minutes': self.minutes,
            'hourly_rate': self.hourly_rate,

        }

    def json_simplify(self):
        return {
            'id': self.pk,
            'job': self.job.id,
            'service': self.service.id,
        }