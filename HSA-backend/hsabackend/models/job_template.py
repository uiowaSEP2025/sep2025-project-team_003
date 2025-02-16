from django.db import models
from hsabackend.models.service import Service
from hsabackend.models.organization import Organization

class JobTemplate(models.Model):
    """A preset template that can be used by an organization to create jobs"""
    description = models.CharField(200)
    service = models.ManyToManyField(Service)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<JobTemplate, id:{self.pk}>"
    