from rest_framework import serializers
from ..models.job import Job, JobsServices
from .service_serializer import ServiceSerializer

class JobServiceSerializer(serializers.ModelSerializer):
    fee = serializers.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        model = JobsServices
        fields = ['job','service', 'fee']

    def create(self, validated_data):
        """
        Create and return a new JobServices instance with services, given the validated data.
        """
        service = validated_data.pop('service')
        job = validated_data.pop('job')
        fee = validated_data.pop('fee', service.default_fee)
        request = JobsServices.objects.create(
                job=job,
                service=service,
                fee=fee,
        )

        return request

    def update(self, instance, validated_data):
        """
        Update and return an existing Job instance with services, given the validated data.
        """
        instance.job = validated_data.get('job', instance.job)
        instance.service = validated_data.get('service', instance.service)
        instance.fee = validated_data.get('fee', instance.fee)

        instance.save()
        return instance
