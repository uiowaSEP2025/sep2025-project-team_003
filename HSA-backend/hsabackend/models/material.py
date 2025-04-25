from curses.ascii import isblank

from django.db import models
from hsabackend.models.model_validators import isNonEmpty
from hsabackend.models.organization import Organization

class Material(models.Model):
    """A physical object used in fulfillment of a job"""
    name = models.CharField(max_length=100,validators=[isNonEmpty])
    description = models.CharField(max_length=200, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    default_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)

    def __str__(self):
        return f"<Material, name: {self.material_name}, organization: {self.organization}>"
    
    def json(self):
        return {
            'id': self.pk,
            'name': self.material_name,
            'description': self.material_description,
            'default_cost': self.default_cost,
        }