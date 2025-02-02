from django.db import models
from service import Service
from request import Request

class ServiceRequest(models.Model):
    serviceID = models.ForeignKey(Service)
    requestID = models.ForeignKey(Request)