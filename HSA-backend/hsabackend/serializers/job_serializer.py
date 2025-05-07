from rest_framework import serializers
from rest_framework.fields import HiddenField

from .contractor_serializer import ContractorSerializer
from .customer_serializer import CustomerSerializer
from .invoice_serializer import InvoiceSerializer
from .material_serializer import MaterialSerializer
from .organization_serializer import OrganizationSerializer
from .service_serializer import ServiceSerializer
from ..models.job import Job


class JobBookingDataSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    contractors = ContractorSerializer(many=True, read_only=True)
    class Meta:
        model = Job
        fields = ['id','job_status','start_date','end_date','description','requestor_address','requestor_city','requestor_state','requestor_zip']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['data'] = {
        'id': instance.id,
        'customerName': instance.customer.first_name + " " + instance.customer.last_name,
        'description': instance.description,
        'jobStatus' : instance.job_status,
        'startDate' : instance.start_date,
        'endDate' : instance.end_date,
        'requestorAddress' : instance.requestor_address,
        'requestorCity' : instance.requestor_city,
        'requestorState' : instance.requestor_state,
        'requestorZip' : instance.requestor_zip
        }
        return representation

class JobTableSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Job
        fields = ['id','description', 'customer', 'job_status', 'start_date', 'end_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['customer'] = f"{instance.customer.first_name} {instance.customer.last_name}"
        return representation








class JobSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    contractors = ContractorSerializer(many=True, read_only=True)
    invoice = InvoiceSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    fee = serializers.DecimalField(decimal_places=2, max_digits=10, allow_null=True, default=0)

    class Meta:
        model = Job
        fields = "__all__"

    def to_representation(self, instance):
        """
        Override to_representation to provide a simplified representation for list views
        """
        representation = {}

        # Add a simplified customer name for display in tables
        if instance.customer:
            representation['customerName'] = f"{instance.customer.first_name} {instance.customer.last_name}"
            representation['customerID'] = instance.customer.id

        # Truncate description if it's too long
        if instance.description:
            description = instance.description
            if len(description) > 50:
                representation['description'] = description[:50] + "..."
            else:
                representation['description'] = description
        representation['id'] = instance.id
        representation['jobStatus'] = instance.job_status
        representation['startDate'] = instance.start_date
        representation['endDate'] = instance.end_date
        representation['requestorAddress'] = instance.requestor_address
        representation['requestorCity'] = instance.requestor_city
        representation['requestorState'] = instance.requestor_state
        representation['requestorZip'] = instance.requestor_zip

        return representation

    def create(self, validated_data):
        """
        Create and return a new Job instance, given the validated data.
        """
        request = Job.objects.create(**validated_data)

        return request

    def update(self, instance, validated_data):
        """
        Update and return an existing Job instance, given the validated data.
        """

        instance.job_status = validated_data.get('job_status', instance.job_status)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.description = validated_data.get('description', instance.description)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.invoice = validated_data.get('invoice', instance.invoice)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.requestor_city = validated_data.get('requestor_city', instance.requestor_city)
        instance.requestor_state = validated_data.get('requestor_state', instance.requestor_state)
        instance.requestor_zip = validated_data.get('requestor_zip', instance.requestor_zip)
        instance.requestor_address = validated_data.get('requestor_address', instance.requestor_address)
        instance.use_hourly_rate = validated_data.get('use_hourly_rate', instance.use_hourly_rate)
        instance.minutes_worked = validated_data.get('minutes_worked', instance.minutes_worked)
        instance.hourly_rate = validated_data.get('hourly_rate', instance.hourly_rate)

        instance.save()
        return instance
