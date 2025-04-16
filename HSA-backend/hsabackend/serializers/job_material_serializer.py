from rest_framework import serializers
from ..models.job import Job
from .material_serializer import MaterialSerializer

class JobMaterialSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)

    class Meta:
        model = Job
        fields = 'materials'

    def to_representation(self, instance):
        """
        Override to_representation to include material details
        """
        representation = super().to_representation(instance)

        # Include material details if available
        if hasattr(instance, 'material') and instance.material:
            representation['material_name'] = instance.material.name
            representation['material_description'] = instance.material.description
            representation['material_unit'] = instance.material.unit

        return representation
