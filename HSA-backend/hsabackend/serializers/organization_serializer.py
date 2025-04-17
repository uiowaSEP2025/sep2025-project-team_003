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
        instance.org_requester_state = validated_data.get('org_requester_state', instance.org_requester_state)
        instance.org_requester_zip = validated_data.get('org_requester_zip', instance.org_requester_zip)
        instance.org_requester_address = validated_data.get('org_requester_address', instance.org_requester_address)
        instance.org_phone = validated_data.get('org_phone', instance.org_phone)
        instance.org_owner_first_name = validated_data.get('org_owner_first_name', instance.org_owner_first_name)
        instance.org_owner_last_name = validated_data.get('org_owner_last_name', instance.org_owner_last_name)
        instance.owning_User = validated_data.get('owning_User', instance.owning_User)
        instance.is_onboarding = validated_data.get('is_onboarding', instance.is_onboarding)
        instance.save()
        return instance
