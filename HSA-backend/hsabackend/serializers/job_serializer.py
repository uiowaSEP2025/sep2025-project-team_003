from rest_framework import serializers

from .contractor_serializer import ContractorSerializer
from .customer_serializer import CustomerSerializer
from .invoice_serializer import InvoiceSerializer
from .material_serializer import MaterialSerializer
from .organization_serializer import OrganizationSerializer
from .service_serializer import ServiceSerializer
from ..models.job import Job, JobsServices, JobsMaterials


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

    def services_representation(self, instance):
        services_data = JobsServices.objects.select_related("service").filter(job=instance.pk)
        services_json = []
        for i in services_data:
            services_json.append({
                "serviceID": i.service.id,
                "serviceName": i.service.name,
                "serviceDescription": i.service.description,
                "fee": i.fee
                            })
        return {"services": services_json}

    def contractors_representation(self, instance):
        contractors_temp = instance.contractors.all()
        contractors_data = ContractorSerializer(contractors_temp, many=True).data
        contractors_json = []
        for i in contractors_data:
            contractors_json.append({
                "contractorID": i['id'],
                "contractorName": i['first_name'] + " " + i['last_name'],
                "contractorPhoneNo": i['phone'],
                "contractorEmail": i['email']
            })
        return {"contractors": contractors_json}

    def materials_representation(self, instance):
        materials = JobsMaterials.objects.select_related("material").filter(job=instance.id)
        materials_json = []
        for i in materials:
            materials_json.append({
                "materialID": i.material.id,
                "materialName": i.material.name,
                "unitsUsed": i.quantity,
                "pricePerUnit": i.unit_price
            })
        return {"materials": materials_json}

    def to_representation(self, instance):
        """
        Override to_representation to provide a simplified representation for list views
        """
        representation = {}

        # Add a simplified customer name for display in tables
        if instance.customer:
            representation['customerName'] = f"{instance.customer.first_name} {instance.customer.last_name}"

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
        representation['requestorAddress'] = instance.job_address
        representation['requestorCity'] = instance.job_city
        representation['requestorState'] = instance.job_state
        representation['requestorZip'] = instance.job_zip

        return representation

    def create(self, validated_data):
        """
        Create and return a new Job instance, given the validated data.
        """
        services_temp = validated_data.pop('services', [])
        contractors_temp = validated_data.pop('contractors', [])
        materials_temp = validated_data.pop('materials', [])
        request = Job.objects.create(**validated_data)

        if services_temp:
            request.services.set(services_temp)
        if contractors_temp:
            request.contractors.set(contractors_temp)
        if materials_temp:
            request.materials.set(materials_temp)

        return request

    def update(self, instance, validated_data):
        """
        Update and return an existing Job instance, given the validated data.
        """

        materials_temp = validated_data.pop('materials', [])
        services_temp = validated_data.pop('services', [])
        contractors_temp = validated_data.pop('contractors', [])
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
        if services_temp is not None:
            instance.services.set(services_temp)
        if materials_temp is not None:
            instance.materials.set(materials_temp)
        if contractors_temp is not None:
            instance.contractors.set(contractors_temp)

        instance.save()
        return instance
