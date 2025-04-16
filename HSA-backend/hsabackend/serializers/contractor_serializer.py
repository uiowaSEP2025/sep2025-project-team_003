from rest_framework import serializers

from hsabackend.models.contractor import Contractor


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = "__all__"