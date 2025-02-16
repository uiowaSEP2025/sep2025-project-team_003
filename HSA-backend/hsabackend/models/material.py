from django.db import models
from hsabackend.models.model_validators import isNonEmpty
from hsabackend.models.organization import Organization

class Material(models.Model):
    """A physical object used in fulfillment of a job"""
    material_name = models.CharField(max_length=100,validators=[isNonEmpty])
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Material, name: {self.material_name}, organization: {self.organization}>"
    