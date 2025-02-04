from django.db import models
from . import customer

class Inovice(models.Model):
    """A bill sent to a customer from an organization on a monthly basis"""
    issuance_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField
    price = models.FloatField()
    customer = models.ForeignKey(customer.Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Invoice, customer: {self.customer}, price: {self.price}>"
    