from django.db import models
from service import Service
from job_template import JobTemplate

class JobTemplate(models.Model):
    """A preset template that can be used by an organization to create jobs"""
    description = models.CharField(200)
    job_template = models.ManyToManyField(JobTemplate)

    def __str__(self):
        return f"<Quote, job: {self.jobID}>"
    