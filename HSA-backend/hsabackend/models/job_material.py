from django.db import models

from hsabackend.models.material import Material
from hsabackend.utils.string_formatters import format_currency

class JobMaterial(models.Model):
    """join table with price details"""
    price_per_unit = models.DecimalField(max_digits=9, decimal_places=2) 
    units_used = models.IntegerField()
    job = models.ForeignKey('hsabackend.Job', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return f"<JobsMaterials, id:{self.pk}>"
    
    def json(self):
        return {
            'id': self.pk,
            'materialID': self.material.pk,
            'materialName': self.material.material_name,
            'unitsUsed': self.units_used,
            'pricePerUnit': self.price_per_unit 
        }