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
    due_date = models.DateField(null=True,blank=True, default=None)
    status = models.CharField(max_length=50, choices=status_choices, default="created")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Invoice, customer: {self.customer}>"
    
    def json(self):
        return {
            "status": self.status,
            "due_date": "None" if self.due_date == None else self.due_date,
            "customer": f"{self.customer.first_name}, {self.customer.last_name}" 
        }