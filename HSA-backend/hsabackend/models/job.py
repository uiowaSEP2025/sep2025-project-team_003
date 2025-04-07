from django.db import models
from hsabackend.models.organization import Organization
from hsabackend.models.model_validators import isNonEmpty, validate_state
from hsabackend.models.customer import Customer
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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    requestor_city = models.CharField(max_length=50, validators=[isNonEmpty])
    requestor_state = models.CharField(max_length=50, validators=[isNonEmpty, validate_state])
    requestor_zip = models.CharField(max_length=10, validators=[isNonEmpty])
    requestor_address = models.CharField(max_length=100, validators=[isNonEmpty])

    def __str__(self):
        return f"<Job, organization: {self.organization}, description: {self.description}>"
    

    def json(self):
        return {
            'id': self.pk,
            'jobStatus': self.job_status,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'description': self.description,
            'customerName': self.customer.first_name + " " + self.customer.last_name,
            'customerID': self.customer.id,
            'requestorAddress': self.requestor_address,
            "requestorCity": self.requestor_city,
            "requestorState": self.requestor_state,
            "requestorZip": self.requestor_zip
        }
    
    def json_simplify(self):
        return {
            'id': self.pk,
            # cap at 50 so table doesn't stretch
        
            'description': self.description[:50] + ("..." if len(self.description) > 50 else ""),
            'job_status': self.job_status,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'customer_name': self.customer.first_name + " " + self.customer.last_name,
        }