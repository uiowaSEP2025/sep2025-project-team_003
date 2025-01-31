from django.db import models
from . import service, job

class ServiceJob(models.Model):
    job_ID = models.ForeignKey(job.Job)
    service_ID = models.ForeignKey(service.Service)
    