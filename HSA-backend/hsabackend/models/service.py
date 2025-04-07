from django.db import models
from hsabackend.models.organization import Organization
from hsabackend.models.model_validators import isNonEmpty

class Service(models.Model):
    """A service offered by an organization. e.g. Lawn care"""
    service_name = models.CharField(max_length=100, validators=[isNonEmpty])
    service_description = models.CharField(max_length=200, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    default_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)

    def __str__(self):
        return f"<Service, service_name: {self.service_name}, owning_org: {self.organization}>"
    
    def json(self):
        return {
            'id': self.pk,
            'service_name': self.service_name,
            'service_description': self.service_description,
            'default_hourly_rate': self.default_hourly_rate,
        }