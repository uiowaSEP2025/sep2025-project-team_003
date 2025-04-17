from django.db import models

from hsabackend.models.material import Material
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service


class JobTemplate(models.Model):
    """A preset template that can be used by an organization to create jobs"""
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, blank=True)
    materials = models.ManyToManyField(Material, blank=True)

    def __str__(self):
        return f"<Job, organization: {self.organization}, description: {self.description}>"

    def json(self):
        return {
            'id': self.pk,
            'description': self.description,

        }

    def json_simplify(self):
        return {
            'id': self.pk,
            # cap at 50 so the table doesn't stretch

            'description': self.description[:50] + ("..." if len(self.description) > 50 else ""),

        }