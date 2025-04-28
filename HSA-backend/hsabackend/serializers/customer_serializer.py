from rest_framework import serializers

from hsabackend.models.customer import Customer
from hsabackend.serializers.organization_serializer import OrganizationSerializer

class CustomerTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id","first_name","last_name","email","phone", "notes"]

class CustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(min_length=1, max_length=50, required=True)
    last_name = serializers.CharField(min_length=1,max_length=50, required=True)
    email = serializers.EmailField(max_length=100, required=True)
    phone = serializers.CharField(max_length=13, required=True)

    class Meta:
        model = Customer
        fields = ["id","first_name","last_name","email","phone", "notes"]

    def create(self, validated_data):
        """
        Create and return a new Customer instance, given the validated data.
        """
        validated_data['phone'] = (validated_data['phone']).replace("-","")
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Customer instance, given the validated data.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = (validated_data.get('phone', instance.phone)).replace("-","")
        instance.notes = validated_data.get('notes', instance.notes)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()
        return instance
