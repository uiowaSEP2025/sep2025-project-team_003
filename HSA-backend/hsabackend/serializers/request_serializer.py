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
        services = validated_data.pop('services', None)

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
        instance.availability = validated_data.get('availability', instance.availability)
        instance.request_status = validated_data.get('request_status', instance.request_status)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.job = validated_data.get('job', instance.job)

        # Update services if provided
        if services is not None:
            instance.services.set(services)

        instance.save()
        return instance
