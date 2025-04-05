from django.db import models
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.material import Material
from hsabackend.utils.string_formatters import format_currency

class JobTemplateMaterial(models.Model):
    """join table with price details"""
    price_per_unit = models.DecimalField(max_digits=9, decimal_places=2) 
    units_used = models.IntegerField()
    job_template = models.ForeignKey(JobTemplate, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return f"<JobTemplatesMaterials, id:{self.pk}>"
    
    def json(self):
        return {
            'id': self.pk,
            'materialID': self.material.pk,
            'materialName': self.material.material_name,
            'unitsUsed': self.units_used,
            'pricePerUnit': self.price_per_unit 
        }
    
    def invoice_material_row(self):
        return {
            "material name": self.material.material_name,
            "per unit": self.price_per_unit,
            "units used": self.units_used,
            "total": (self.price_per_unit * self.units_used)
        }