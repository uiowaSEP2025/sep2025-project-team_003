from django.db import models
from . import organization, model_validators
class Contractor(models.Model):
    """A person employed by a organization to fulfill a job"""
    first_name = models.CharField(max_length=50, validators=[model_validators.isNonEmpty])
    last_name = models.CharField(max_length=50, validators=[model_validators.isNonEmpty])
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10, validators=[model_validators.isValidPhone])
    organization = models.ForeignKey(organization.Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Contractor: {self.pk}>"
    