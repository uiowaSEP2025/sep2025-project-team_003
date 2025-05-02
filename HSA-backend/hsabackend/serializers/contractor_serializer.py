from rest_framework import serializers

from hsabackend.models.contractor import Contractor
from hsabackend.serializers.organization_serializer import OrganizationSerializer

class ContractorTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ["id","first_name","last_name","email","phone"]

class ContractorSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    first_name = serializers.CharField(min_length=1, max_length=50, required=True)
    last_name = serializers.CharField(min_length=1,max_length=50, required=True)
    email = serializers.EmailField(max_length=100, required=True)
    phone = serializers.CharField(max_length=13, required=True)

    class Meta:
        model = Contractor
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new Contractor instance, given the validated data.
        """

        return Contractor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Contractor instance, given the validated data.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = (validated_data.get('phone', instance.phone)).replace("-","")
        instance.save()
        return instance
