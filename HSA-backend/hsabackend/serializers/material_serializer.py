from rest_framework import serializers

from hsabackend.models.material import Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"