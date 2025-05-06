from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.db import transaction
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.models.customer import Customer
from hsabackend.models.service import Service
from hsabackend.models.material import Material
from hsabackend.models.contractor import Contractor
from hsabackend.models.job import Job
from hsabackend.models.job_service import JobService
from hsabackend.models.job_material import JobMaterial
from hsabackend.models.job_contractor import JobContractor

@api_view(["GET"])
@check_authenticated_and_onboarded(require_onboarding=False)
def getOrganizationDetail(request):
    try:
        org = request.org
        return Response(org.json(), status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error":"An error occured trying to get organization. Please make sure you have created an organization."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def editOrganizationDetail(request):
    org = request.org
    name = request.data.get('name', org.org_name)
    email = request.data.get('email', org.org_email)
    city = request.data.get('city', org.org_city)
    phone = request.data.get('phone', org.org_phone)
    requestor_state = request.data.get('requestorState', org.org_requestor_state)
    requestor_zip = request.data.get('requestorZip', org.org_requestor_zip)
    requestor_address = request.data.get('requestorAddress', org.org_requestor_address)
    ownerFn = request.data.get('ownerFn', org.org_owner_first_name)
    ownerLn = request.data.get('ownerLn', org.org_owner_last_name)
    
    org.org_name = name
    org.org_email = email
    org.org_city = city
    org.org_requestor_state = requestor_state
    org.org_requestor_zip = requestor_zip
    org.org_requestor_address = requestor_address
    org.org_phone = phone
    org.org_owner_first_name = ownerFn
    org.org_owner_last_name = ownerLn
    
    try:
        org.full_clean()
        org.save()
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "Organization details updated successfully."}, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def complete_onboarding(request):
    org = request.org

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
                new_customer = Customer(
                    first_name = customer_request.get('firstn'),
                    last_name = customer_request.get('lastn'),
                    email = customer_request.get('email'),
                    phone_no = customer_request.get('phoneno').replace("-", ""),
                    notes = customer_request.get('notes'),
                    organization = org
                )
                new_customer.full_clean()
                new_customer.save()
            
            if service_request:
                new_service = Service(
                    service_name = service_request.get('service_name'),
                    service_description = service_request.get('service_description'),
                    organization = org
                )
                new_service.full_clean()
                new_service.save()
            
            if material_request:
                new_material = Material(
                    material_name = material_request.get('material_name'),
                    organization = org
                )
                new_material.full_clean()
                new_material.save()

            if contractor_request:
                new_contractor = Contractor(
                    first_name = contractor_request.get('firstName'),
                    last_name = contractor_request.get('lastName'),
                    email = contractor_request.get('email'),
                    phone = contractor_request.get('phone').replace("-", ""),
                    organization = org
                )
                new_contractor.full_clean()
                new_contractor.save()

            if job_request:
                new_job = Job(
                    job_status = "created",
                    start_date = job_request.get("startDate"),
                    end_date = job_request.get("endDate"),
                    description = job_request.get("description"),
                    organization = org,
                    customer = new_customer,
                    requestor_address = job_request.get("address"),
                    requestor_city = job_request.get("city"),
                    requestor_state = job_request.get("state"),
                    requestor_zip = job_request.get("zip"),
                    flat_fee = job_request.get("flatfee"),
                    hourly_rate = job_request.get("hourlyrate"),
                    minutes_worked = job_request.get("minutesworked")

                )
                new_job.full_clean()
                new_job.save()

                # Add service and job join entry
                service_list = job_request.get("services") or []
                for service in service_list:
                    new_job_service = JobService(
                        job = new_job,
                        service = new_service
                    )
                    new_job_service.full_clean()
                    new_job_service.save()
                
                # Add material and job join entry
                material_list = job_request.get("materials") or []
                for material in material_list:
                    new_material_job = JobMaterial(
                        material = new_material,
                        job = new_job,
                        units_used = material["unitsUsed"],
                        price_per_unit = material["pricePerUnit"]
                    )
                    new_material_job.full_clean()
                    new_material_job.save()
                
                # Add contractor and job join entry
                contractor_list = job_request.get("contractors") or []
                for contractor in contractor_list:
                    new_job_contractor = JobContractor(
                        job = new_job,
                        contractor = new_contractor
                    )

                    new_job_contractor.full_clean()
                    new_job_contractor.save()  

            org.is_onboarding = is_onboarding
            org.save()
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Onboarding complete"}, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def createOrganization(request):
    # users can only have a single organization
    org_count = Organization.objects.filter(owning_User=request.user.pk).count()
    if org_count > 0:
        return Response({"errors": "This user already has an organization"}, status=status.HTTP_400_BAD_REQUEST)

    name = request.data.get('name', '')
    email = request.data.get('email', '')
    city = request.data.get('city', '')
    phone = request.data.get('phone', '').replace("-","")
    requestor_state = request.data.get('requestorState', '')
    requestor_zip = request.data.get('requestorZip', '')
    requestor_address = request.data.get('requestorAddress', '')

    ownerFn = request.data.get('ownerFn', '')
    ownerLn = request.data.get('ownerLn', '')

    owning_User = request.user

    try:
        the_organization = Organization(
            org_name = name,
            org_email = email,
            org_city = city,
            org_requestor_state = requestor_state,
            org_requestor_zip = requestor_zip,
            org_phone=phone,
            org_requestor_address = requestor_address,
            org_owner_first_name = ownerFn,
            org_owner_last_name = ownerLn,
            owning_User = owning_User,
        )
        the_organization.full_clean()
        the_organization.save()

    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Organization created"}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def deleteOrganization(request):
    # This API is unreachable due to the fact that one login must have exactly one org, may be used in the future

    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        org_count = Organization.objects.filter(owning_User=request.user.pk).count()
        if org_count <= 1:
            return Response({"errors": "All users must have at least 1 org; You only have 1 or less orgs, cannot delete."}, status=status.HTTP_400_BAD_REQUEST)
        
        # code coverage here is wanky due to the fact that the delete path will never get walked under normal app circumstances.
        # because a user should never be left without an org.
        Organization.objects.filter(owning_User=request.user.pk).delete()
        return Response({"message": "Organization deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":f"An error occured trying to delete organization. Please contact admin. Error: {e}"}, status=status.HTTP_400_BAD_REQUEST)
