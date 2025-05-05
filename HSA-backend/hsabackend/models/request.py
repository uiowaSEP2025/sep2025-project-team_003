from django.db import models

from hsabackend.models.job import Job
from hsabackend.models.model_validators import is_non_empty, validate_state, is_valid_phone
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service


class Request(models.Model):
    """A request for service that a potential customer creates"""
    status_choices = [
        ('received', 'received'),
        ('approved', 'approved'),
    ]
    requester_first_name    = models.CharField(max_length=100, validators=[is_non_empty])
    requester_last_name     = models.CharField(max_length=100, validators=[is_non_empty])
    requester_email         = models.CharField(max_length=100)
    requester_city          = models.CharField(max_length=50, validators=[is_non_empty])
    requester_state         = models.CharField(max_length=50, validators=[is_non_empty, validate_state])
    requester_zip           = models.CharField(max_length=10, validators=[is_non_empty])
    requester_address       = models.CharField(max_length=100, validators=[is_non_empty])
    requester_phone         = models.CharField(max_length=10, blank=True, validators=[is_valid_phone])
    description             = models.CharField(max_length=200, validators=[is_non_empty])
    availability            = models.CharField(max_length=200, validators=[is_non_empty])
    request_status          = models.CharField(max_length=50, choices=status_choices, default="received")
    organization            = models.ForeignKey(Organization, on_delete=models.CASCADE)
    job                     = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"<Request, name: {self.requester_first_name} {self.requester_last_name}, address: {self.requester_address}>"
    
    def json(self):
        return {
            'id': self.id,
            'requester_first_name': self.requester_first_name,
            'requester_last_name': self.requester_last_name,
            'requester_email': self.requester_email,
            'requester_city': self.requester_city,
            'requester_state': self.requester_state,
            'requester_zip': self.requester_zip,
            'requester_address': self.requester_address,
            'description': self.description,
            'status': self.status
        }
    
    def json_simplify(self):
        return {
            'id': self.id,
            'requestor_name': self.requestor_first_name + " " + self.requestor_last_name,
            'requestor_email': self.requestor_email,
            'description': self.description,
        }