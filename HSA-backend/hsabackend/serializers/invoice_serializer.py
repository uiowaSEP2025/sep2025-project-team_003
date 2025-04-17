from rest_framework import serializers

from hsabackend.serializers.discount_serializer import DiscountSerializer
from hsabackend.models.invoice import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    discounts = DiscountSerializer(many=True, read_only=True)
    class Meta:
        model = Invoice
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new Invoice instance, given the validated data.
        """
        return Invoice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Invoice instance, given the validated data.
        """
        instance.issuance_date = validated_data.get('issuance_date', instance.issuance_date)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.status = validated_data.get('status', instance.status)
        instance.tax = validated_data.get('tax', instance.tax)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.save()
        return instance
