from curses.ascii import isblank

from django.db import models
from hsabackend.models.model_validators import isNonEmpty
from hsabackend.models.organization import Organization

class Material(models.Model):
    """A physical object used in fulfillment of a job"""
    material_name = models.CharField(max_length=100,validators=[isNonEmpty])
    material_description = models.CharField(max_length=200, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Material, name: {self.material_name}, organization: {self.organization}>"
    
    def json(self):
        return {
            'id': self.pk,
            'material_name': self.material_name,
            'material_description': self.material_description,
        }