from django.db import models
from hsabackend.models.customer import Customer
from hsabackend.models.discount import Discount
from hsabackend.models.job import Job
from hsabackend.utils.string_formatters import format_maybe_null_date

class Invoice(models.Model):
    """A bill sent to a customer from an organization on a monthly basis"""
    status_choices = [
        ('created', 'created'),
        ('issued', 'issued'),
        ('paid','paid')
    ]
 
    date_issued = models.DateField(null=True,blank=True, default=None)
    date_due = models.DateField(null=True,blank=True, default=None)
    status = models.CharField(max_length=50, choices=status_choices, default="created")
    sales_tax_percent = models.DecimalField(max_digits=2, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    discounts = models.ManyToManyField(Discount, blank=True)


    @property
    def subtotal(self):
        running_sub = 0
        jobs = Job.objects.filter(invoice=self.pk)
        for job in jobs:
            running_sub += job.subtotal
        return running_sub

    @property
    def discounted_subtotal(self):
        total_discount = 0
        for discount in self.discounts.all():
            total_discount += discount.discount_percent
        return self.subtotal * total_discount

    @property
    def subtotal_after_discount(self):
        return self.subtotal - self.discounted_subtotal

    @property
    def taxable_amount(self):
        return self.subtotal_after_discount * (self.sales_tax_percent / 100)

    @property
    def total(self):
        return self.subtotal_after_discount + self.taxable_amount


    def __str__(self):
        return f"<Invoice, customer: {self.customer}>"
    
    def json_for_view_invoice(self):
        return {
            "id": self.pk,
            "status": self.status,
            "dueDate": "N/A" if self.due_date == None else self.due_date,
            "issuanceDate": "N/A" if self.issuance_date == None else self.issuance_date,
            "customer": f"{self.customer.first_name}, {self.customer.last_name}"
        }
    
    def json(self):
        return {
            "id": self.pk,
            "status": self.status,
            "due_date": format_maybe_null_date(self.due_date),
            "issuance_date": format_maybe_null_date(self.issuance_date),
            "customer_id": {self.customer.id},
            "customer_name": f"{self.customer.first_name}, {self.customer.last_name}",
            "tax": str(self.tax)
        }