from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from django.db.models import Q
from django.core.exceptions import ValidationError
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded

@api_view(["GET"])
@check_authenticated_and_onboarded(require_onboarding=False)
def getOrganizationDetail(request):
    # single get instead of list (as users only get 1 org)

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
    requestor_state = request.data.get('requestorState', org.org_requester_state)
    requestor_zip = request.data.get('requestorZip', org.org_requester_zip)
    requestor_address = request.data.get('requestorAddress', org.org_requester_address)
    ownerFn = request.data.get('ownerFn', org.org_owner_first_name)
    ownerLn = request.data.get('ownerLn', org.org_owner_last_name)
    
    org.org_name = name
    org.org_email = email
    org.org_city = city
    org.org_requester_state = requestor_state
    org.org_requester_zip = requestor_zip
    org.org_requester_address = requestor_address
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



    try:
        org.fullclean()
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
