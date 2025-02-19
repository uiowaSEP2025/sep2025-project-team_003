from django.db import models
from hsabackend.models.model_validators import isValidPhone, isNonEmpty
from hsabackend.models.organization import Organization

class Customer(models.Model):
    """A person that has a pending or fulfilled job"""
    first_name = models.CharField(50, validators=[isNonEmpty])
    last_name = models.CharField(50, validators=[isNonEmpty])
    email = models.EmailField(max_length=100)
    phone_no = models.CharField(max_length=10, validators=[isValidPhone])
    notes = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Customer: {self.pk}>"
    
    def json(self):
                return {
            'id': self.pk,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_no': self.phone_no,
            'notes': self.notes,
        }