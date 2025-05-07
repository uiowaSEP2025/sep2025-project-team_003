from rest_framework import serializers

from hsabackend.models.invoice import Invoice
from hsabackend.serializers.customer_serializer import CustomerSerializer
from hsabackend.serializers.discount_serializer import DiscountSerializer
from hsabackend.utils.get_data_helpers import get_jobs_for_invoice


class InvoiceTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id','customer','issuance_date','due_date','status', 'tax', 'payment_link']

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "customer": instance.customer.first_name + " " + instance.customer.last_name,
            "customer_id": instance.customer.id,
            "issuance_date": instance.issuance_date,
            "due_date": instance.due_date,
            "status": instance.status,
            "tax": instance.tax,
            "payment_link": instance.payment_link,
        }
        return representation


class InvoiceSerializer(serializers.ModelSerializer):
    discounts = DiscountSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Invoice
        fields = "__all__"

    def to_representation(self, instance):
        customer = CustomerSerializer(instance.customer)
        discounts = DiscountSerializer(instance.discounts, many=True)
        jobs = get_jobs_for_invoice(instance.pk)

        representation = {}
        representation['id'] = instance.pk
        representation['dateIssued'] = instance.date_issued
        representation['dateDue'] = instance.date_due
        representation['status'] = instance.status
        representation['paymentLink'] = instance.payment_link
        representation['tax'] = instance.tax
        representation['customer'] = customer.data
        representation['discounts'] = discounts.data
        representation['jobs'] = jobs
        return representation

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
        instance.tax = validated_data.get('tax', instance.tax)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.payment_link = validated_data.get('payment_link', instance.payment_link)
        instance.save()
        return instance
