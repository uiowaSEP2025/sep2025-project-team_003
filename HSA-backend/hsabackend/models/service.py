from django.db import models
from organization import Organization

class Service(models.Model):
    """A service offered by an organization. Eg. Lawn care"""
    service_name = models.CharField(max_length=100)
    service_description = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Service, service_name: {self.service_name}, owning_org: {self.organization}>"
    