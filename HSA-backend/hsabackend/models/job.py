from decimal import Decimal

from django.core.serializers import serialize
from django.db import models
from hsabackend.models.contractor import Contractor
from hsabackend.models.customer import Customer
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
        ('rejected', 'rejected'),
    ]

    job_status = models.CharField(max_length=50, choices=status_choices, default="created")
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.CharField(max_length=200, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    invoice = models.ForeignKey('hsabackend.Invoice', null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, blank=True, through='JobsServices')
    materials = models.ManyToManyField(Material, blank=True, through='JobsMaterials')
    contractors = models.ManyToManyField(Contractor, blank=True)
    job_city = models.CharField(max_length=50, validators=[isNonEmpty])
    job_state = models.CharField(max_length=50, validators=[isNonEmpty, validate_state])
    job_zip = models.CharField(max_length=10, validators=[isNonEmpty])
    job_address = models.CharField(max_length=100, validators=[isNonEmpty])
    use_hourly_rate = models.BooleanField(default=False)
    minutes_worked = models.IntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def __str__(self):
        return f"<Job, organization: {self.organization}, description: {self.description}>"

    def get_default_labor_rate(self):
        return self.organization.default_labor_rate

    @property
    def subtotal(self):
        running_sub = 0
        services = self.services.all()
        materials = self.materials.all()
        for service in services:
            running_sub += service.fee
        for material in materials:
            running_sub += material.quantity * material.unit_price
        if self.use_hourly_rate:
            Decimal(self.minutes_worked / 60) * self.hourly_rate
        return running_sub

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
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
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
    fee = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    class Meta:
        db_table = 'hsabackend_job_services'

    def __str__(self):
        return (f"<Job, Service, Fee:"
                f" Job: {self.job},"
                f" Service: {self.service},"
                f" Hourly Rate: {self.fee}")

    def json(self):
        return {
            'id': self.pk,
            'job': self.job.id,
            'service': self.service.id,
            'fee': self.fee,

        }

    def json_simplify(self):
        return {
            'id': self.pk,
            'job': self.job.id,
            'service': self.service.id,
        }
