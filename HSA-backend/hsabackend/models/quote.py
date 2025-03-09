from django.db import models
from hsabackend.models.discount_type import DiscountType
from hsabackend.models.job import Job
from hsabackend.models.invoice import Invoice

class Quote(models.Model):
    """The price for a job that the organization sends to the customer for approval"""
    status_choices = [
        ('created', 'created'),
        ('accepted', 'accepted'),
    ]

    issuance_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=status_choices, default="created")
    material_subtotal = models.FloatField()
    total_price = models.FloatField()
    jobID = models.OneToOneField(Job, on_delete= models.CASCADE)
    discount_type = models.ForeignKey(DiscountType, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"<Quote, job: {self.jobID}>"
    