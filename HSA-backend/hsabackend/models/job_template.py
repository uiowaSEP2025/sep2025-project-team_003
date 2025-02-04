from django.db import models
from . import service
class JobTemplate(models.Model):
    """A preset template that can be used by an organization to create jobs"""
    description = models.CharField(200)
    job_template = models.ManyToManyField(service.Service)

    def __str__(self):
        return f"<Quote, job: {self.jobID}>"
    