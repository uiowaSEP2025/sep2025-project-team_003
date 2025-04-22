from rest_framework import serializers

from .material_serializer import MaterialSerializer
from .organization_serializer import OrganizationSerializer
from .service_serializer import ServiceSerializer
from ..models.job_template import JobTemplate


class JobTemplateSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = JobTemplate
        fields = "__all__"

    def to_representation(self, instance):
        """
        Override to_representation to provide a simplified representation for list views
        """
        representation = super().to_representation(instance)

        # Add a simplified customer name for display in tables
        if instance.customer:
            representation['customer_name'] = f"{instance.customer.first_name} {instance.customer.last_name}"

        # Truncate description if it's too long
        if 'description' in representation and representation['description']:
            description = representation['description']
            if len(description) > 50:
                representation['description_display'] = description[:50] + "..."
            else:
                representation['description_display'] = description

        return representation

    def create(self, validated_data):
        """
        Create and return a new Job Template instance, given the validated data.
        """
        services_temp = validated_data.pop('services', [])
        materials_temp = validated_data.pop('materials', [])
        request = JobTemplate.objects.create(**validated_data)

        if services_temp:
            request.service.set(services_temp)
        if materials_temp:
            request.materials.set(materials_temp)

        return request

    def update(self, instance, validated_data):
        """
        Update and return an existing Job Template instance, given the validated data.
        """

        materials_temp = validated_data.pop('materials', [])
        services_temp = validated_data.pop('services', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.organization = validated_data.get('organization', instance.organization)
        if services_temp is not None:
            instance.services.set(services_temp)
        if materials_temp is not None:
            instance.materials.set(materials_temp)

        instance.save()
        return instance
