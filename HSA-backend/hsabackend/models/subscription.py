from django.db import models
from hsabackend.models.job_template import JobTemplate

class Subscription(models.Model):
    """An agreement between an organization and a customer to recieve monthly service"""
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=9, decimal_places=2) 
    job_template = models.ForeignKey(JobTemplate, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Subscription, description: {self.description}>"
    