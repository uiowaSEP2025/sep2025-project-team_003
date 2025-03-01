from django.db import models
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.models.model_validators import isNonEmpty, validate_state, isValidPhone

class Request(models.Model):
    """A request for service that a potential customer creates"""
    status_choices = [
        ('received', 'received'),
        ('approved', 'approved'),
    ]

    requestor_first_name = models.CharField(max_length=100,validators=[isNonEmpty])
    requestor_last_name = models.CharField(max_length=100,validators=[isNonEmpty])
    requestor_email = models.CharField(max_length=100)
    requestor_city = models.CharField(max_length=50,validators=[isNonEmpty])
    requestor_state = models.CharField(max_length=50,validators=[isNonEmpty,validate_state])
    requestor_zip = models.CharField(max_length=10,validators=[isNonEmpty])
    requestor_address = models.CharField(max_length=100,validators=[isNonEmpty])
    requestor_phone_no = models.CharField(max_length=10, validators=[isValidPhone])
    description = models.CharField(max_length=200, validators=[isNonEmpty])
    status = models.CharField(max_length=50, choices=status_choices, default="received") 
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    service = models.ManyToManyField(Service)

    def __str__(self):
        return f"<Request, name: {self.requestor_name}, address: {self.requestor_address}>"
    
    def json(self):
        return {
            'id': self.id,
            'requestor_name': self.requestor_name,
            'requestor_email': self.requestor_email,
            'requestor_city': self.requestor_city,
            'requestor_state': self.requestor_state,
            'requestor_zip': self.requestor_zip,
            'requestor_address': self.requestor_address,
            'description': self.description,
            'status': self.status
        }