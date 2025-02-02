from django.db import models

class Organization(models.Model):
    """The organization managed by a handyman"""
    org_name = models.CharField(max_length=100)
    org_email = models.CharField(max_length=100)
    org_address = models.CharField(max_length=100)
    org_owner_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"<Organization, org_name: {self.org_name}>"
    