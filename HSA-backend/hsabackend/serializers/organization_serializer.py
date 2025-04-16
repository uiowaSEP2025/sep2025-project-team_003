from rest_framework import serializers

from hsabackend.models.organization import Organization

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = "__all__"