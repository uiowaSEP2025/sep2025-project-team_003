from rest_framework import serializers

from hsabackend.models.contractor import Contractor


class ContractorSerializer(serializers.ModelSerializer):
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
        instance.phone = validated_data.get('phone', instance.phone)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()
        return instance
