from django.db import models
from hsabackend.models.job import Job
from hsabackend.models.material import Material

class MaterialJob(models.Model):
    unit_cost = models.FloatField()
    units_used = models.IntegerField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)