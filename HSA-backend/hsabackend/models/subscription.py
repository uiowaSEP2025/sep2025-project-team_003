from django.db import models
from . import job_template

class Subscription(models.Model):
    """An agreement between an organization and a customer to recieve monthly service"""
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    job_template = models.ForeignKey(job_template.JobTemplate, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Subscription, description: {self.description}>"
    