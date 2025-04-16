from rest_framework import serializers

from hsabackend.models.discount import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"