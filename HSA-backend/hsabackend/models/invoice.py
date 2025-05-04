import decimal

from django.db import models
from hsabackend.models.customer import Customer
from hsabackend.models.discount import Discount
from hsabackend.utils.string_formatters import format_maybe_null_date

class Invoice(models.Model):
    """A bill sent to a customer from an organization monthly"""
    status_choices = [
        ('created', 'created'),
        ('issued', 'issued'),
        ('paid','paid')
    ]
 
    date_issued = models.DateField(null=True,blank=True, default=None)
    date_due = models.DateField(null=True,blank=True, default=None)
    status = models.CharField(max_length=50, choices=status_choices, default="created")
    sales_tax_percent = models.DecimalField(max_digits=5, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    discounts = models.ManyToManyField(Discount, blank=True)
    payment_link = models.URLField(max_length=200, blank=True)


    @property
    def subtotal(self):
        running_sub = 0
        jobs = Job.objects.filter(invoice=self.pk)
        for job in jobs:
            running_sub += job.subtotal
        return running_sub

    @property
    def discount_aggregate_percentage(self):
        discount_percentage = 0
        for discount in self.discounts.all():
            discount_percentage += discount.discount_percent
        return discount_percentage

    @property
    def discounted_subtotal(self):
                return self.subtotal * self.discount_aggregate_percentage / 100

    @property
    def subtotal_after_discount(self):
        return self.subtotal - self.discounted_subtotal

    @property
    def taxable_amount(self):
        return decimal.Decimal(self.subtotal_after_discount) * self.sales_tax_percent

    @property
    def total(self):
        return decimal.Decimal(self.subtotal_after_discount) + self.taxable_amount


    def __str__(self):
        return f"<Invoice, customer: {self.customer}>"
    
    def json_for_view_invoice(self):
        return {
            "id": self.pk,
            "status": self.status,
            "dueDate": "N/A" if self.date_due == None else self.date_due,
            "issuanceDate": "N/A" if self.date_issued == None else self.date_issued,
            "customer": f"{self.customer.first_name}, {self.customer.last_name}"
        }
    
    def json(self):
        return {
            "id": self.pk,
            "status": self.status,
            "due_date": format_maybe_null_date(self.date_due),
            "issuance_date": format_maybe_null_date(self.date_issued),
            "customer_id": {self.customer.id},
            "customer_name": f"{self.customer.first_name}, {self.customer.last_name}",
            "tax": str(self.sales_tax_percent)
        }