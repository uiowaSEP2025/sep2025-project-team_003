from rest_framework import serializers
from ..models.job import Job, JobsServices
from .service_serializer import ServiceSerializer

class JobServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['services']

    def to_representation(self, instance):
        """
        Override to_representation to include service details
        """
        representation = super().to_representation(instance)

        # Include service details if available
        if hasattr(instance, 'service') and instance.service:
            representation['service_name'] = instance.service.name
            representation['service_description'] = instance.service.description

        return representation

    def create(self, validated_data):
        """
        Create and return a new Job instance with services, given the validated data.
        """
        services_data = validated_data.pop('services', [])
        job = Job.objects.create(**validated_data)

        # Add services to the job
        for service_data in services_data:
            service = service_data.get('service')
            minutes = service_data.get('minutes', 0)
            hourly_rate = service_data.get('hourly_rate', 0)

            JobsServices.objects.create(
                job=job,
                service=service,
                minutes=minutes,
                hourly_rate=hourly_rate
            )

        return job

    def update(self, instance, validated_data):
        """
        Update and return an existing Job instance with services, given the validated data.
        """
        services_data = validated_data.pop('services', None)

        # Update job fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update services if provided
        if services_data is not None:
            # Clear existing services
            JobsServices.objects.filter(job=instance).delete()

            # Add new services
            for service_data in services_data:
                service = service_data.get('service')
                minutes = service_data.get('minutes', 0)
                hourly_rate = service_data.get('hourly_rate', 0)

                JobsServices.objects.create(
                    job=instance,
                    service=service,
                    minutes=minutes,
                    hourly_rate=hourly_rate
                )

        instance.save()
        return instance
