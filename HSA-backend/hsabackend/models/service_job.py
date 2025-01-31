from django.db import models
from . import job,service

class ServiceJob(models.Model):
    job_ID = models.ForeignKey(job.Job, on_delete=models.CASCADE)
    service_ID = models.ForeignKey(service.Service, on_delete=models.CASCADE)
    