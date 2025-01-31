from django.db import models

class Service(models.Model):
    service_name = models.CharField(max_length=100)
    service_description = models.CharField(max_length=200)