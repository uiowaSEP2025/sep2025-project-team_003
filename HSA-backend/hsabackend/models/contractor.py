from django.db import models
from organization import Organization

class Contractor(models.Model):
    """A person employed by a organization to fulfill a job"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    organization = models.ManyToOneRel(Organization)

    def __str__(self):
        return f"<Contractor, organization: {self.organization}, first_name: {self.first_name}, last_name: {self.last_name}>"
    