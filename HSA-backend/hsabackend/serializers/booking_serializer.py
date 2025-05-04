from rest_framework import serializers

from hsabackend.models.booking import Booking
from hsabackend.serializers.job_serializer import JobSerializer
from hsabackend.serializers.organization_serializer import OrganizationSerializer

class BookingSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new Booking instance, given the validated data.
        """

        return Booking.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Booking instance, given the validated data.
        """
        instance.event_name = validated_data.get('event_name', instance.event_name)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.booking_type = validated_data.get('booking_type', instance.booking_type)
        instance.back_color = validated_data.get('back_color', instance.back_color)
        instance.status = validated_data.get('status', instance.status)
        instance.job = validated_data.get('job', instance.job)
        instance.save()
        return instance
