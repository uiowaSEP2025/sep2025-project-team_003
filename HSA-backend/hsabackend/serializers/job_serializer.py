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
