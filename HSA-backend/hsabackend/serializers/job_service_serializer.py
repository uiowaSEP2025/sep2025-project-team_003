from rest_framework import serializers
from ..models.job import Job
from .service_serializer import ServiceSerializer

class JobServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Job
        fields = 'services'

    def to_representation(self, instance):
        """
        Override to_representation to include service details
        """
        representation = super().to_representation(instance)

        # Include service details if available
        if hasattr(instance, 'service') and instance.service:
            representation['service_name'] = instance.service.name
            representation['service_description'] = instance.service.description

        return representation
