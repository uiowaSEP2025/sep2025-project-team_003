from rest_framework import serializers

from hsabackend.models.request import Request


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new Request instance, given the validated data.
        """
        services = validated_data.pop('service', [])
        request = Request.objects.create(**validated_data)

        # Add services to the request
        if services:
            request.service.set(services)

        return request

    def update(self, instance, validated_data):
        """
        Update and return an existing Request instance, given the validated data.
        """
        services = validated_data.pop('service', None)

        # Update request fields
        instance.requester_first_name = validated_data.get('requester_first_name', instance.requester_first_name)
        instance.requester_last_name = validated_data.get('requester_last_name', instance.requester_last_name)
        instance.requester_email = validated_data.get('requester_email', instance.requester_email)
        instance.requester_city = validated_data.get('requester_city', instance.requester_city)
        instance.requester_state = validated_data.get('requester_state', instance.requester_state)
        instance.requester_zip = validated_data.get('requester_zip', instance.requester_zip)
        instance.requester_address = validated_data.get('requester_address', instance.requester_address)
        instance.requester_phone = validated_data.get('requester_phone', instance.requester_phone)
        instance.description = validated_data.get('description', instance.description)
        instance.request_status = validated_data.get('request_status', instance.request_status)
        instance.organization = validated_data.get('organization', instance.organization)

        # Update services if provided
        if services is not None:
            instance.service.set(services)

        instance.save()
        return instance
