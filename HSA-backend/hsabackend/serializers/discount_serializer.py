from rest_framework import serializers

from hsabackend.models.discount import Discount
from hsabackend.serializers.organization_serializer import OrganizationSerializer


class DiscountSerializer(serializers.ModelSerializer):
    discount_name = serializers.CharField(min_length=1, max_length=100, required=True)
    discount_percent = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)

    class Meta:
        model = Discount
        fields = ['discount_name','id','discount_percent']

    def create(self, validated_data):
        """
        Create and return a new Discount instance, given the validated data.
        """
        return Discount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Discount instance, given the validated data.
        """
        instance.discount_name = validated_data.get('discount_name', instance.discount_name)
        instance.discount_percent = validated_data.get('discount_percent', instance.discount_percent)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()
        return instance
