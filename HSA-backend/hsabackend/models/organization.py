from django.db import models
from . import model_validators
from django.contrib.auth.models import User

class Organization(models.Model):
    """The organization managed by a handyman"""
    org_name = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    org_email = models.EmailField(max_length=100)
    org_city = models.CharField(max_length=50, validators=[model_validators.isNonEmpty])
    org_requestor_state = models.CharField(max_length=50, validators=[model_validators.isNonEmpty, model_validators.validate_state])
    org_requestor_zip = models.CharField(max_length=10, validators=[model_validators.isNonEmpty])
    org_requestor_address = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    org_phone = models.CharField(max_length=10, validators=[model_validators.isValidPhone])
    org_owner_first_name = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    org_owner_last_name = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    owning_User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Organization, org_name: {self.org_name}>"

    def json(self):
        return {
            'org_name': self.org_name,
            'org_email': self.org_email,
            'org_city': self.org_city,
            'org_requestor_state': self.org_requestor_state,
            'org_requestor_zip': self.org_requestor_zip,
            'org_requestor_address': self.org_requestor_address,
            'org_owner_first_name': self.org_owner_first_name,
            'org_owner_last_name': self.org_owner_last_name,
            'owning_User': self.owning_User.id if self.owning_User else None
        }


    