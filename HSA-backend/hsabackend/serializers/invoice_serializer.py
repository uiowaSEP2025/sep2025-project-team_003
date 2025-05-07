from rest_framework import serializers

from hsabackend.models.customer import Customer
from hsabackend.models.job import Job
from hsabackend.serializers.customer_serializer import CustomerSerializer
from hsabackend.serializers.discount_serializer import DiscountSerializer
from hsabackend.models.invoice import Invoice
from hsabackend.utils.get_data_helpers import get_jobs_for_invoice

class InvoiceTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id','customer','date_issued','date_due','status', 'sales_tax_percent', 'payment_link']

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "customer": instance.customer.first_name + " " + instance.customer.last_name,
            "customer_id": instance.customer.id,
            "date_issued": instance.date_issued,
            "date_due": instance.date_due,
            "status": instance.status,
            "sales_tax_percent": instance.sales_tax_percent,
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
        representation['salesTaxPercent'] = instance.sales_tax_percent
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
        instance.sales_tax_percent = validated_data.get('sales_tax_percent', instance.sales_tax_percent)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.payment_link = validated_data.get('payment_link', instance.payment_link)
        instance.save()
        return instance
