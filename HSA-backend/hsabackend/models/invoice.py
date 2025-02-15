from django.db import models
from hsabackend.models.customer import Customer

class Invoice(models.Model):
    """A bill sent to a customer from an organization on a monthly basis"""
    status_choices = [
        ('created', 'created'),
        ('issued', 'issued'),
        ('paid','paid')
    ]

    issuance_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=status_choices, default="created")
    price = models.FloatField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Invoice, customer: {self.customer}, price: {self.price}>"
    