from django.db import models
from . import organization, model_validators

class DiscountType(models.Model):
    """A named percentage discount to be defined by the organization"""
    discount_name = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    discount_percent = models.FloatField()
    organization = models.ForeignKey(organization.Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<DiscountType, organization: {self.organization}, percent: {self.discount_percent}>"
    