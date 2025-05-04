from rest_framework import serializers

from .job_serializer import JobSerializer
from ..models.job import Job, JobsMaterials
from .material_serializer import MaterialSerializer

class JobMaterialSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)

    class Meta:
        model = JobsMaterials
        fields = '__all__'
