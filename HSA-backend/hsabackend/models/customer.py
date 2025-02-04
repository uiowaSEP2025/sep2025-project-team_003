from django.db import models
from . import organization, model_validators

class Customer(models.Model):
    """A person that has a pending or fulfilled job"""
    first_name = models.CharField(50, validators=[model_validators.isNonEmpty])
    last_name = models.CharField(50, validators=[model_validators.isNonEmpty])
    email = models.EmailField(max_length=100)
    phone_no = models.CharField(max_length=10, validators=[model_validators.isValidPhone])
    notes = models.CharField(max_length=200)
    organization = models.ForeignKey(organization.Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Customer: {self.pk}>"
    