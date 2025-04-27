from rest_framework import serializers

from hsabackend.models.service import Service
from hsabackend.serializers.organization_serializer import OrganizationSerializer


class ServiceSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name','description','default_fee', 'organization']
    def to_representation(self, instance):
        """
        Override to_representation to provide a simplified representation for list views
        """
        representation = super().to_representation(instance)
        representation['serviceName'] = instance.name
        representation['serviceDescription'] = instance.description
        representation['defaultFee'] = instance.default_fee
        return representation

    def create(self, validated_data):
        """
        Create and return a new Service instance, given the validated data.
        """
        return Service.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Service instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.service_name)
        instance.description = validated_data.get('description', instance.service_description)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.default_fee = validated_data.get('default_fee', instance.default_fee)
        instance.save()
        return instance
