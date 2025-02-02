from django.db import models
from organization import Organization

class Customer(models.Model):
    """A person that has a pending or fulfilled job"""
    orginationID = models.ForeignKey(Organization)
    first_name = models.CharField(50)
    last_name = models.CharField(50)
    email = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10)
    notes = models.CharField(max_length=200)

    def __str__(self):
        return f"<Customer, first_name: {self.first_name}, last_name: {self.last_name}, organization: organization>"
    