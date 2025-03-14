from django.db import models
from hsabackend.models.discount_type import DiscountType
from hsabackend.models.job import Job
from hsabackend.models.invoice import Invoice
from hsabackend.utils.description_trunctator import truncate_description_for_table

class Quote(models.Model):
    """The price for a job that the organization sends to the customer for approval"""
    status_choices = [
        ('created', 'created'),
        ('accepted', 'accepted'),
    ]

    issuance_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=status_choices, default="created")
    material_subtotal = models.DecimalField(max_digits=9, decimal_places=2)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)
    jobID = models.OneToOneField(Job, on_delete= models.CASCADE)
    discount_type = models.ForeignKey(DiscountType, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"<Quote, job: {self.jobID}>"
    
    def jsonForInvoiceTable(self):
        return {
            "id": self.id,
            "material_subtotal": self.material_subtotal,
            "total_price": self.total_price,
            "job_description": truncate_description_for_table(self.jobID.description)
        }
    
    def jsonToDisplayForInvoice(self):
        return {
            "materialSubtotal": self.material_subtotal,
            "totalPrice": self.total_price,
            "jobDescription": truncate_description_for_table(self.jobID.description)
        }