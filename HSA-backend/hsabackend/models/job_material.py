from django.db import models
from hsabackend.models.job import Job
from hsabackend.models.material import Material

class JobMaterial(models.Model):
    price_per_unit = models.FloatField()
    units_used = models.IntegerField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return f"<JobsMaterials, id:{self.pk}>"
    
    def json(self):
        return {
            'id': self.pk,
            'job_id': self.job.pk,
            'material_id': self.material.pk,
            'material_name': self.material.material_name,
            'units_used': self.units_used,
            'price_per_unit': self.price_per_unit 
        }