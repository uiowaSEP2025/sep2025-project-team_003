from django.db import models

class MaterialJob(models.Model):
    unit_cost = models.FloatField()
    units_used = models.IntegerField()
    