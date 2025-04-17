from rest_framework import serializers
from ..models.job import Job, JobsMaterials
from .material_serializer import MaterialSerializer

class JobMaterialSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['materials']

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

    def create(self, validated_data):
        """
        Create and return a new Job instance with materials, given the validated data.
        """
        materials_data = validated_data.pop('materials', [])
        job = Job.objects.create(**validated_data)

        # Add materials to the job
        for material_data in materials_data:
            material = material_data.get('material')
            quantity = material_data.get('quantity', 1)
            unit_price = material_data.get('unit_price', 0)

            JobsMaterials.objects.create(
                job=job,
                material=material,
                quantity=quantity,
                unit_price=unit_price
            )

        return job

    def update(self, instance, validated_data):
        """
        Update and return an existing Job instance with materials, given the validated data.
        """
        materials_data = validated_data.pop('materials', None)

        # Update job fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update materials if provided
        if materials_data is not None:
            # Clear existing materials
            JobsMaterials.objects.filter(job=instance).delete()

            # Add new materials
            for material_data in materials_data:
                material = material_data.get('material')
                quantity = material_data.get('quantity', 1)
                unit_price = material_data.get('unit_price', 0)

                JobsMaterials.objects.create(
                    job=instance,
                    material=material,
                    quantity=quantity,
                    unit_price=unit_price
                )

        instance.save()
        return instance
