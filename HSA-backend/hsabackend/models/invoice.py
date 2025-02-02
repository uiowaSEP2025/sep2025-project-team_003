from django.db import models
from customer import Customer

class Inovice(models.Model):
    """A bill sent to a customer from an organization on a monthly basis"""
    issuance_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField
    price = models.FloatField()

    def __str__(self):
        return f"<Invoice, customer: {self.customer}, price: {self.price}>"
    