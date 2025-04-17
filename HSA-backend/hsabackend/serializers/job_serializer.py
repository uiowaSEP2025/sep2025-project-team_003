from rest_framework import serializers

from .contractor_serializer import ContractorSerializer
from .customer_serializer import CustomerSerializer
from .invoice_serializer import InvoiceSerializer
from .material_serializer import MaterialSerializer
from .service_serializer import ServiceSerializer
from ..models.job import Job


class JobSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    contractors = ContractorSerializer(many=True, read_only=True)
    invoice = InvoiceSerializer(read_only=True)

    class Meta:
        model = Job
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
        Create and return a new Job instance, given the validated data.
        """
        return Job.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Job instance, given the validated data.
        """

        materials = validated_data.pop('materials', [])
        services = validated_data.pop('services', [])
        contractors = validated_data.pop('contractors', [])
        instance.job_status = validated_data.get('job_status', instance.job_status)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.description = validated_data.get('description', instance.description)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.invoice = validated_data.get('invoice', instance.invoice)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.job_city = validated_data.get('job_city', instance.job_city)
        instance.job_state = validated_data.get('job_state', instance.job_state)
        instance.job_zip = validated_data.get('job_zip', instance.job_zip)
        instance.job_address = validated_data.get('job_address', instance.job_address)
        instance.use_hourly_rate = validated_data.get('use_hourly_rate', instance.use_hourly_rate)
        instance.minutes_worked = validated_data.get('minutes_worked', instance.minutes_worked)
        instance.hourly_rate = validated_data.get('hourly_rate', instance.hourly_rate)
        if services is not None:
            instance.services.set(services)
        if materials is not None:
            instance.materials.set(materials)
        if contractors is not None:
            instance.contractors.set(contractors)

        instance.save()
        return instance
