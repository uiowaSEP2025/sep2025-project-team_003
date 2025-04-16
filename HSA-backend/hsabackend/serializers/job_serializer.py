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