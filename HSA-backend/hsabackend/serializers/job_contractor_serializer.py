from rest_framework import serializers
from hsabackend.models.job import Job
from .contractor_serializer import ContractorSerializer

class JobContractorSerializer(serializers.ModelSerializer):
    contractor = ContractorSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['contractors']

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

    def create(self, validated_data):
        """
        Create and return a new Job instance with contractors, given the validated data.
        """
        contractors_data = validated_data.pop('contractors', [])
        job = Job.objects.create(**validated_data)

        # Add contractors to the job
        if contractors_data:
            job.contractors.set(contractors_data)

        return job

    def update(self, instance, validated_data):
        """
        Update and return an existing Job instance with contractors, given the validated data.
        """
        contractors_data = validated_data.pop('contractors', None)

        # Update job fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update contractors if provided
        if contractors_data is not None:
            instance.contractors.set(contractors_data)

        instance.save()
        return instance
