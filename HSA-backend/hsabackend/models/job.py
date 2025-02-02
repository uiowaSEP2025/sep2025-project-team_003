from django.db import models
from organization import Organization
from customer import Customer

class Job(models.Model):
    """A request for service from a customer to an organization"""
    job_status = models.CharField(max_length=50)
    start_date = models.DateField
    end_date = models.DateField
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"<Job, organization: {self.organization}, customer: {self.customer}, description: {self.description}>"
    