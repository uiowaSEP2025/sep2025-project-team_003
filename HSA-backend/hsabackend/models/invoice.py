from django.db import models
from . import customer

class Invoice(models.Model):
    customer_id = models.ForeignKey(customer.Customer)
    invoice_date = models.DateField()
    invoice_status = models.CharField(max_length=70) # sent, paid, overdue??
    invoice_price = models.IntegerField()