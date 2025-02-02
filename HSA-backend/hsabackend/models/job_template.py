from django.db import models
from service import Service

class JobTemplate(models.Model):
    """A preset template that can be used by an organization to create jobs"""
    description = models.CharField(200)

    def __str__(self):
        return f"<Quote, job: {self.jobID}>"
    