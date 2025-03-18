from django.db import models
from hsabackend.models.organization import Organization
from hsabackend.models.model_validators import isNonEmpty

class DiscountType(models.Model):
    """A named percentage discount to be defined by the organization"""
    discount_name = models.CharField(max_length=100, validators=[isNonEmpty])
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<DiscountType, organization: {self.organization}, percent: {self.discount_percent}>"
    