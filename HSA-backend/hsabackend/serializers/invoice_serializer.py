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
        instance.date_issued = validated_data.get('date_issued', instance.date_issued)
        instance.date_due = validated_data.get('date_due', instance.date_due)
        instance.status = validated_data.get('status', instance.status)
        instance.sales_tax_percent = validated_data.get('sales_tax_percent', instance.sales_tax_percent)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.payment_link = validated_data.get('payment_link', instance.payment_link)
        instance.save()
        return instance
