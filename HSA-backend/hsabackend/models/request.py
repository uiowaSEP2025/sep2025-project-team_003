from django.db import models
from organization import Organization

class Request(models.Model):
    """A request for service that a potential customer creates"""
    requestor_name = models.CharField(max_length=100)
    requestor_email = models.CharField(max_length=100)
    requestor_city = models.CharField(max_length=50)
    requestor_state = models.CharField(max_length=50)
    requestor_zip = models.CharField(max_length=10)
    requestor_address = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=50) # what are we storing for this field?
    orgID = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Request, name: {self.requestor_name}, address: {self.requestor_address}>"