from django.db import models
from . import model_validators
from django.contrib.auth.models import User

class Organization(models.Model):
    """The organization managed by a handyman"""
    org_name = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    org_email = models.EmailField(max_length=100)
    org_city = models.CharField(max_length=50, validators=[model_validators.isNonEmpty])
    org_state = models.CharField(max_length=50, validators=[model_validators.isNonEmpty, model_validators.validate_state])
    org_zip = models.CharField(max_length=10, validators=[model_validators.isNonEmpty])
    org_address = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    org_phone = models.CharField(max_length=10, validators=[model_validators.isValidPhone])
    org_owner_first_name = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    org_owner_last_name = models.CharField(max_length=100, validators=[model_validators.isNonEmpty])
    owning_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_onboarding = models.BooleanField(default=True)
    default_labor_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=False)
    default_payment_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"<Organization, org_name: {self.org_name}>"

    def json(self):
        return {
            'org_name': self.org_name,
            'org_email': self.org_email,
            'org_phone' : self.org_phone,
            'org_city': self.org_city,
            'org_state': self.org_state,
            'org_zip': self.org_zip,
            'org_address': self.org_address,
            'org_owner_first_name': self.org_owner_first_name,
            'org_owner_last_name': self.org_owner_last_name,
            'owning_user': self.owning_user.id if self.owning_user else None,
            'is_onboarding': self.is_onboarding,
            'default_labor_rate': self.default_labor_rate
        }


    