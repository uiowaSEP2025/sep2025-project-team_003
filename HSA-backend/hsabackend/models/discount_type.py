from django.db import models
from organization import Organization

class DiscountType(models.Model):
    """A named percentage discount to be defined by the organization"""
    discount_name = models.CharField(max_length=100)
    discount_percent = models.FloatField()
    organizationID = models.ManyToOneRel(Organization)

    def __str__(self):
        return f"<DiscountType, organization: {self.organizationID}, percent: {self.discount_percent}>"
    