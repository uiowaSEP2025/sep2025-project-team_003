from django.db import models
from . import customer

class Job(models.Model):
    job_status = models.CharField(max_length=50) # scheduled completed?
    start_date = models.DateField()
    end_date = models.DateField()
    job_description = models.CharField(max_length=200)
    customer_id = models.ForeignKey(customer.Customer)
