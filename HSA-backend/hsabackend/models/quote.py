from django.db import models
from job import Job
from discount_type import DiscountType
from job import Job

class Quote(models.Model):
    """The price for a job that the organization sends to the customer for approval"""
    issuance_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=50)
    material_subtotal = models.IntegerField()
    total_price = models.IntegerField()
    jobID = models.OneToOneField(Job)
    discount_type = models.ManyToOneRel(DiscountType)
    
    def __str__(self):
        return f"<Quote, job: {self.jobID}>"
    