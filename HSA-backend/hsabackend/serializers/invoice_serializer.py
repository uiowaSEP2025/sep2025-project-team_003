from rest_framework import serializers

from hsabackend.serializers.discount_serializer import DiscountSerializer
from hsabackend.models.invoice import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    discounts = DiscountSerializer(many=True, read_only=True)
    class Meta:
        model = Invoice
        fields = "__all__"