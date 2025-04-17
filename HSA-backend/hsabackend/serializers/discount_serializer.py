from rest_framework import serializers

from hsabackend.models.discount import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"

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
