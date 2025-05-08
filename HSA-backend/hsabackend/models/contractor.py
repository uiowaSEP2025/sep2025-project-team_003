from django.db import models
from hsabackend.models.organization import Organization
from hsabackend.models.model_validators import isNonEmpty,isValidPhone
from hsabackend.utils.string_formatters import format_phone_number

class Contractor(models.Model):
    """A person employed by a organization to fulfill a job"""
    first_name = models.CharField(max_length=50, validators=[isNonEmpty])
    last_name = models.CharField(max_length=50, validators=[isNonEmpty])
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10, validators=[isValidPhone])
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Contractor: {self.pk}>"
    
    def name_id_json(self):
        return {
            "id": self.pk,
            "name": f"{self.last_name}, {self.first_name}"
        }

    def json(self):
        return {
            'id': self.pk,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': format_phone_number(self.phone),
        }