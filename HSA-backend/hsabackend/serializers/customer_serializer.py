from rest_framework import serializers

from hsabackend.models.customer import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new Customer instance, given the validated data.
        """
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Customer instance, given the validated data.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()
        return instance
