from rest_framework import serializers
from models.job import Job
from .contractor_serializer import ContractorSerializer

class JobContractorSerializer(serializers.ModelSerializer):
    contractor = ContractorSerializer(read_only=True)

    class Meta:
        model = Job
        fields = 'contractors'

    def to_representation(self, instance):
        """
        Override to_representation to include contractor details
        """
        representation = super().to_representation(instance)

        # Include contractor details if available
        if hasattr(instance, 'contractor') and instance.contractor:
            representation['contractor_name'] = instance.contractor.name
            representation['contractor_phone'] = instance.contractor.phone
            representation['contractor_email'] = instance.contractor.email

        return representation
