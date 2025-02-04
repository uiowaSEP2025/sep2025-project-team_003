from django.db import models
from . import organization, model_validators

class Service(models.Model):
    """A service offered by an organization. Eg. Lawn care"""
    service_name = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    service_description = models.CharField(max_length=200)
    organization = models.ForeignKey(organization.Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Service, service_name: {self.service_name}, owning_org: {self.organization}>"
    