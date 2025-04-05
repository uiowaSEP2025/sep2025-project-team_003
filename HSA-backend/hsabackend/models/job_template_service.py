from django.db import models
from hsabackend.models.service import Service
from hsabackend.models.job_template import JobTemplate

class JobTemplateService(models.Model):
    """Job template service join"""
    job_template = models.ForeignKey(JobTemplate, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"<JobTemplatesServices, id:{self.pk}, jobtemplateid: {self.job_template.pk}, serviceid: {self.service.pk}>"
    
    def json(self):
        return {
            'id': self.pk,
            'serviceID': self.service.id,
            'serviceName': self.service.service_name,
            'serviceDescription': self.service.service_description
        }