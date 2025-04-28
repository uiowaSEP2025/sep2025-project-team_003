from rest_framework import serializers

from hsabackend.models.material import Material
from hsabackend.serializers.organization_serializer import OrganizationSerializer


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ["id", "name", "description", "default_cost"]

    def create(self, validated_data):
        """
        Create and return a new Material instance, given the validated data.
        """
        return Material.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Material instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.default_cost = validated_data.get('default_cost', instance.default_cost)
        instance.save()
        return instance
