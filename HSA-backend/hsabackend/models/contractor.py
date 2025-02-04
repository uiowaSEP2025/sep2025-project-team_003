from django.db import models
from . import organization
class Contractor(models.Model):
    """A person employed by a organization to fulfill a job"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    organization = models.ForeignKey(organization.Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Contractor: {self.pk}>"
    