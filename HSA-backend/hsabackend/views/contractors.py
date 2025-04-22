from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.contractor import Contractor
from django.db.models import Q
from django.core.exceptions import ValidationError
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_contractor_table_data(request):
    org = request.org
    search = request.query_params.get('search', '')
    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset',0)

    if not pagesize or not offset:
        return Response({"message": "missing pagesize or offset"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pagesize = int(pagesize)
        offset = int(offset)
    except:
        return Response({"message": "pagesize and offset must be int"}, status=status.HTTP_400_BAD_REQUEST)
    
    offset = offset * pagesize
    contractors = Contractor.objects.filter(organization=org.pk).filter(
        Q(first_name__icontains=search) | Q(last_name__icontains=search) 
    )[offset:offset + pagesize] if search else Contractor.objects.filter(organization=org.pk)[offset:offset + pagesize]

    data = []
    for cust in contractors:
        data.append(cust.json())
    
    count = Contractor.objects.filter(organization=org.pk).filter(
        Q(first_name__icontains=search) | Q(last_name__icontains=search)
    ).count() if search else Contractor.objects.filter(organization=org.pk).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["GET"])
@check_authenticated_and_onboarded(require_onboarding=False)
def get_contractor_excluded_table_data(request):
    org = request.org
    search = request.query_params.get('search', '')
    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset',0)
    excluded_ids_str = request.GET.getlist('excludeIDs', [])
    excluded_ids = [int(id) for id in excluded_ids_str]

    if not pagesize or not offset:
        return Response({"message": "missing pagesize or offset"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pagesize = int(pagesize)
        offset = int(offset)
    except:
        return Response({"message": "pagesize and offset must be int"}, status=status.HTTP_400_BAD_REQUEST)
    
    offset = offset * pagesize
    contractors = Contractor.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).filter(
        Q(first_name__icontains=search) | Q(last_name__icontains=search) 
    )[offset:offset + pagesize] if search else Contractor.objects.filter(organization=org.pk).exclude(id__in=excluded_ids)[offset:offset + pagesize]

    data = []
    for cust in contractors:
        data.append(cust.json())
    
    count = Contractor.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).filter(
        Q(first_name__icontains=search) | Q(last_name__icontains=search)
    ).count() if search else Contractor.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)
    
@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def create_contractor(request):
    org = request.org

    first_name = request.data.get('firstName', '')
    last_name = request.data.get('lastName', '')
    email = request.data.get('email', '')
    phone = request.data.get('phone', '').replace("-","")

    contractor = Contractor(
        first_name = first_name,
        last_name = last_name,
        email = email,
        phone = phone,
        organization = org,
    )

    try:
        contractor.full_clean()  # Validate the model instance
        contractor.save()
        return Response({"message": "Contractor created successfully", "data": contractor.json()}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_contractor(request, id):
    org = request.org
    contractor_qs = Contractor.objects.filter(pk=id, organization=org)

    if not contractor_qs.exists():
        return Response({"message": "The contractor does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    contractor = contractor_qs[0]

    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    email = request.data.get('email', '')
    phone = request.data.get('phone', '')

    contractor.first_name = first_name
    contractor.last_name = last_name
    contractor.email = email
    contractor.phone = phone.replace("-",'')
    
    try:
        contractor.full_clean()  # Validate the model instance
        contractor.save()
        return Response({"message": "Contractor edited successfully"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def delete_contractor(request, id):
    org = request.org
    cust = Contractor.objects.filter(pk=id, organization=org)

    if not cust.exists():
        return Response({"message": "The contractor does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    cust[0].delete()

    return Response({"message": "Contractor deleted successfully"}, status=status.HTTP_200_OK)
