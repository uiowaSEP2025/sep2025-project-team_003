from django.db import models
from hsabackend.models.discount_type import DiscountType
from hsabackend.models.job import Job
from hsabackend.models.invoice import Invoice
from hsabackend.utils.string_formatters import truncate_description_for_table, format_address, format_date_to_iso_string
from decimal import Decimal

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
    total_price = models.DecimalField(max_digits=9, decimal_places=2) # undiscounted price
    jobID = models.OneToOneField(Job, on_delete= models.CASCADE)
    discount_type = models.ForeignKey(DiscountType, null=True, on_delete=models.SET_NULL)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"<Quote, job: {self.jobID}>"
    
    
    def jsonForInvoiceTable(self):  # the mini table on invoice/id
        return {
            "id": self.id,
            "material_subtotal": self.material_subtotal,
            "total_price": self.total_price,
            "job_description": truncate_description_for_table(self.jobID.description)
        }
    
    def jsonToDisplayForInvoice(self): # for update/create invoice
        return {
            "materialSubtotal": self.material_subtotal,
            "totalPrice": self.total_price,
            "jobDescription": truncate_description_for_table(self.jobID.description),
        }
    
    def geerate_invoice_global_table_json(self): # for pdf invoice
        return {
            "Date": format_date_to_iso_string(self.jobID.end_date),
            "Job Description": self.jobID.description,
            "Address": format_address(self.jobID.requestor_address, self.jobID.requestor_city, self.jobID.requestor_state, self.jobID.requestor_zip),
            "Total Undiscounted": self.total_price,
            "Discount Percent": self.discount_type.discount_percent if self.discount_type.discount_percent else Decimal(0)
        }