from django.db import models
from hsabackend.models.organization import Organization

class JobTemplate(models.Model):
    """A preset template that can be used by an organization to create jobs"""
    description = models.CharField(200)
    name = models.CharField(200, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"<JobTemplate, id:{self.pk}>"
    
    def json(self):
        return {
            'id': self.pk,
            # cap at 50 so table doesn't stretch
            'name': self.name,
            'description': self.description[:50] + ("..." if len(self.description) > 50 else ""),
        }