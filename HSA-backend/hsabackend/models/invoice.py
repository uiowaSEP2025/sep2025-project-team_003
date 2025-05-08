from django.db import models
from hsabackend.models.customer import Customer
from hsabackend.utils.string_formatters import format_maybe_null_date
import hsabackend.models.model_validators as model_validators

class Invoice(models.Model):
    """A bill sent to a customer from an organization on a monthly basis"""
    status_choices = [
        ('created', 'created'),
        ('issued', 'issued'),
        ('paid','paid')
    ]
 
    issuance_date = models.DateField(null=True,blank=True, default=None)
    due_date = models.DateField(null=True,blank=True, default=None)
    status = models.CharField(max_length=50, choices=status_choices, default="created")
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_url = models.CharField(max_length=300, validators=[model_validators.isNonEmpty, model_validators.is_valid_http_url], blank=True, null=True)
 
    def __str__(self):
        return f"<Invoice, customer: {self.customer}>"
    
    def json_for_view_invoice(self):
        return {
            "id": self.pk,
            "status": self.status,
            "dueDate": "N/A" if self.due_date == None else self.due_date,
            "issuanceDate": "N/A" if self.issuance_date == None else self.issuance_date,
            "customer": f"{self.customer.first_name}, {self.customer.last_name}",
            "url": self.payment_url
        }
    
    def json(self):
        return {
            "id": self.pk,
            "status": self.status,
            "due_date": format_maybe_null_date(self.due_date),
            "issuance_date": format_maybe_null_date(self.issuance_date),
            "customer": f"{self.customer.first_name}, {self.customer.last_name}",
            "tax": str(self.tax)
        }