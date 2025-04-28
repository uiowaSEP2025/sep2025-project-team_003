from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.contractor import Contractor
from hsabackend.models.customer import Customer
from hsabackend.models.job import Job
from hsabackend.models.material import Material
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.serializers.contractor_serializer import ContractorSerializer
from hsabackend.serializers.customer_serializer import CustomerSerializer
from hsabackend.serializers.job_serializer import JobSerializer
from hsabackend.serializers.material_serializer import MaterialSerializer
from hsabackend.serializers.organization_serializer import OrganizationSerializer
from hsabackend.serializers.service_serializer import ServiceSerializer
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded


@api_view(["GET"])
@check_authenticated_and_onboarded(require_onboarding=False)
def get_organization(request):
    org = request.organization
    serializer = OrganizationSerializer(org)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_organization(request):
    org = request.organization
    org_data = {
        "org_name": request.data.get("orgName", ""),
        "org_email": request.data.get("orgEmail", ""),
        "org_city": request.data.get("orgCity", ""),
        "org_phone": request.data.get("orgPhone", "").replace("-", ""),
        "org_state": request.data.get("orgState", ""),
        "org_zip": request.data.get("orgZip", ""),
        "org_address": request.data.get("orgAddress", ""),
        "org_owner_first_name": request.data.get("orgOwnerFirstName", ""),
        "org_owner_last_name": request.data.get("orgOwnerLastName", ""),
        "default_labor_rate": request.data.get("defaultLaborRate", ""),
        "default_payment_link": request.data.get("defaultPaymentLink", "")
    }

    serializer = OrganizationSerializer(org, data=org_data, partial=True)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.update(org, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def complete_onboarding(request):
    org = request.organization

    if not org.is_onboarding:
        return Response({"message": "Already onboarded"}, status=status.HTTP_400_BAD_REQUEST)
    
    is_onboarding = request.data.get("isOnboarding")

    customer_request = request.data.get("customerRequest")
    service_request = request.data.get("serviceRequest")
    material_request = request.data.get("materialRequest")
    contractor_request = request.data.get("contractorRequest")
    job_request = request.data.get("jobRequest")

    if customer_request is None or service_request is None or job_request is None:
        return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            org.full_clean()

            if customer_request:
                customer_data = {
                    "first_name"      : customer_request.get('firstn'),
                    "last_name"       : customer_request.get('lastn'),
                    "email"           : customer_request.get('email'),
                    "phone"        : customer_request.get('phoneno').replace("-", ""),
                    "notes"           : customer_request.get('notes'),
                    "organization"    : org
                }
                customer_serializer = CustomerSerializer(data=customer_data)
                customer_serializer.is_valid(raise_exception=True)
                customer_serializer.save()
            
            if service_request:
                service_data = {
                    "service_name" : service_request.get('service_name'),
                    "service_description" : service_request.get('service_description'),
                    "organization" : org
                }

                service_serializer = ServiceSerializer(data=service_data)
                service_serializer.is_valid(raise_exception=True)
                service_serializer.save()
            
            if material_request:
                material_data = {
                    "material_name" : material_request.get('material_name'),
                    "material_description" : material_request.get('material_description'),
                    "default_cost": material_request.get('default_cost'),
                    "organization" : org
                }

                material_serializer = MaterialSerializer(data=material_data)
                material_serializer.is_valid(raise_exception=True)
                material_serializer.save()

            if contractor_request:
                contractor_data = {
                    "first_name" : contractor_request.get('firstName'),
                    "last_name" : contractor_request.get('lastName'),
                    "email" : contractor_request.get('email'),
                    "phone" : contractor_request.get('phone').replace("-", ""),
                    "organization" : org
                }

                contractor_serializer = ContractorSerializer(data=contractor_data)
                contractor_serializer.is_valid(raise_exception=True)
                contractor_serializer.save()

            if job_request:
                job_data = {
                    "job_status"      : "created",
                    "start_date"      : job_request.get("startDate"),
                    "end_date"        : job_request.get("endDate"),
                    "description"     : job_request.get("description"),
                    "organization"    : org,
                    "customer"        : customer_serializer.instance if customer_serializer.is_valid() else None,
                    "job_address"     : job_request.get("address"),
                    "job_city"        : job_request.get("city"),
                    "job_state"       : job_request.get("state"),
                    "job_zip"         : job_request.get("zip"),
                    "services"        : job_request.get("services"),
                    "materials"       : job_request.get("materials"),
                    "contractors"     : job_request.get("contractors"),
                    "use_hourly_rate" : job_request.get("useHourlyRate"),
                    "hourly_rate"     : job_request.get("hourlyRate"),
                    "minutes_worked"  : job_request.get("minutesWorked"),
                }

                job_serializer = JobSerializer(data=job_data)
                job_serializer.is_valid(raise_exception=True)
                job_serializer.save()
            org.is_onboarding = is_onboarding
            org.save()
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Onboarding complete"}, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def create_organization(request):
    # users can only have a single organization
    org_count = Organization.objects.filter(owning_user=request.user.pk).count()
    if org_count > 0:
        return Response({"errors": "This user already has an organization"}, status=status.HTTP_400_BAD_REQUEST)

    org_data = {
        "org_name": request.data.get("orgName", ""),
        "org_email": request.data.get("orgEmail", ""),
        "org_city": request.data.get("orgCity", ""),
        "org_phone": request.data.get("orgPhone", "").replace("-", ""),
        "org_state": request.data.get("orgState", ""),
        "org_zip": request.data.get("orgZip", ""),
        "org_address": request.data.get("orgAddress", ""),
        "org_owner_first_name": request.data.get("orgOwnerFirstName", ""),
        "org_owner_last_name": request.data.get("orgOwnerLastName", ""),
        "default_labor_rate": request.data.get("defaultLaborRate", ""),
        "default_payment_link": request.data.get("defaultPaymentLink", ""),
        "owning_user":  request.user
    }

    try:
        serializer = OrganizationSerializer(data=org_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Organization created"}, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def delete_organization(request):
    try:
        org_count = Organization.objects.filter(owning_user=request.user.pk).count()
        if org_count <= 1:
            return Response({"errors": "All users must have at least 1 org; You only have 1 or less orgs, cannot delete."}, status=status.HTTP_400_BAD_REQUEST)
        
        # code coverage here is wanky because the delete path will never get walked under normal app circumstances.
        # because a user should never be left without an org.
        Organization.objects.filter(owning_user=request.user.pk).delete()
        return Response({"message": "Organization deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":f"An error occurred trying to delete organization. Please contact admin. Error: {e}"}, status=status.HTTP_400_BAD_REQUEST)
