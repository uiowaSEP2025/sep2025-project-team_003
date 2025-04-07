from django.db import models
from hsabackend.models.organization import Organization
from hsabackend.models.model_validators import isNonEmpty, is_valid_percent
from hsabackend.utils.string_formatters import format_percent

class Discount(models.Model):
    """A named percentage discount to be defined by the organization"""
    discount_name = models.CharField(max_length=100, validators=[isNonEmpty])
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, validators=[is_valid_percent])
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Discount, organization: {self.organization}, percent: {self.discount_percent}>"
    

    def json_for_discount_table(self):
        return {
            "id": self.pk, 
            "discount_name": self.discount_name,
            "discount_percent": format_percent(self.discount_percent)
        }