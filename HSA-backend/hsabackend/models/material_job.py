from django.db import models
from . import material,Job

class MaterialJob(models.Model):
    unit_cost = models.FloatField()
    units_used = models.IntegerField()
    job = models.ForeignKey(Job.Job, on_delete=models.CASCADE)
    material = models.ForeignKey(material.Material, on_delete=models.CASCADE)