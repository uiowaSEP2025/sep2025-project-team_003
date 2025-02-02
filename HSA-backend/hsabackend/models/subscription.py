from django.db import models
from customer import Customer
from job_template import JobTemplate

class Subscription(models.Model):
    """An agreement between an organization and a customer to recieve monthly service"""
    description = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return f"<Subscription, customer: {self.customerID}, description: {self.description}>"
    