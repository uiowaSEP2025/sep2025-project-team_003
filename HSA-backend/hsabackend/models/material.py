from django.db import models
from . import organization

class Material(models.Model):
    """A physical object used in fulfillment of a job"""
    material_name = models.CharField(max_length=100)
    organization = models.ForeignKey(organization.Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Material, name: {self.material_name}, organization: {self.organization}>"
    