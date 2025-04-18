from rest_framework import serializers

from hsabackend.models.organization import Organization

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new Organization instance, given the validated data.
        """
        return Organization.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Organization instance, given the validated data.
        """
        instance.org_name = validated_data.get('org_name', instance.org_name)
        instance.org_email = validated_data.get('org_email', instance.org_email)
        instance.org_city = validated_data.get('org_city', instance.org_city)
        instance.org_state = validated_data.get('org_state', instance.org_state)
        instance.org_zip = validated_data.get('org_zip', instance.org_zip)
        instance.org_address = validated_data.get('org_address', instance.org_address)
        instance.org_phone = validated_data.get('org_phone', instance.org_phone)
        instance.org_owner_first_name = validated_data.get('org_owner_first_name', instance.org_owner_first_name)
        instance.org_owner_last_name = validated_data.get('org_owner_last_name', instance.org_owner_last_name)
        instance.owning_user = validated_data.get('owning_user', instance.owning_user)
        instance.is_onboarding = validated_data.get('is_onboarding', instance.is_onboarding)
        instance.default_labor_rate = validated_data.get('default_labor_rate', instance.default_labor_rate)
        instance.default_payment_link = validated_data.get('default_payment_link', instance.default_payment_link)
        instance.save()
        return instance
