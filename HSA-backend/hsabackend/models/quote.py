from django.db import models
from . import job

class Quote(models.Model):
    job_ID = models.ForeignKey(job.Job)
    quote_date = models.DateField()
    quote_status = models.CharField(max_length=100) # quoted accepted
    price = models.IntegerField()