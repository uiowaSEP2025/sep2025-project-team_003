from django.db import models
from . import model_validators

class Organization(models.Model):
    """The organization managed by a handyman"""
    org_name = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    org_email = models.EmailField(max_length=100)
    org_city = models.CharField(max_length=50, validators=[model_validators.isNonEmpty])
    org_requestor_state = models.CharField(max_length=50, validators=[model_validators.isNonEmpty])
    org_requestor_zip = models.CharField(max_length=10, validators=[model_validators.isNonEmpty])
    org_requestor_address = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    org_owner_first_name = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    org_owner_last_name = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    
    def __str__(self):
        return f"<Organization, org_name: {self.org_name}>"
    