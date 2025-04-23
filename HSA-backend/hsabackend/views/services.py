from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.service import Service
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_service_table_data(request):
    org = request.org
    search = request.query_params.get('search', '')
    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset', 0)
    
    if not pagesize or not offset:
        return Response({"message": "missing pagesize or offset"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pagesize = int(pagesize)
        offset = int(offset)
    except:
        return Response({"message": "pagesize and offset must be int"}, status=status.HTTP_400_BAD_REQUEST)
    
    offset = offset * pagesize
    services = Service.objects.filter(organization=org.pk).filter(
        Q(service_name__icontains=search) | Q(service_description__icontains=search) 
    )[offset:offset + pagesize] if search else Service.objects.filter(organization=org.pk)[offset:offset + pagesize]

    data = []
    for service in services:
        data.append(service.json())
    
    count = Service.objects.filter(organization=org.pk).filter(
        Q(service_name__icontains=search) | Q(service_description__icontains=search)
    ).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["GET"])
@check_authenticated_and_onboarded(require_onboarding=False)
def get_service_excluded_table_data(request):
    org = request.org
    search = request.query_params.get('search', '')
    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset', 0)
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
    services = Service.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).filter(
        Q(service_name__icontains=search) | Q(service_description__icontains=search) 
    )[offset:offset + pagesize] if search else Service.objects.filter(organization=org.pk).exclude(id__in=excluded_ids)[offset:offset + pagesize]

    data = []
    for service in services:
        data.append(service.json())
    
    count = Service.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).filter(
        Q(service_name__icontains=search) | Q(service_description__icontains=search)
    ).count() if search else Service.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).count()

    res = {
        'data': data,
        'totalCount': count
    }    

    return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def create_service(request):
    org = request.org
    service_name = request.data.get('service_name', '')
    service_description = request.data.get('service_description', '')

    service = Service(
        service_name = service_name,
        service_description = service_description,
        organization = org
    )

    try:
        service.full_clean()  # Validate the model instance
        service.save()
        return Response({"message": "Service created successfully", "data": service.json()}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_service(request, id):
    org = request.org
    service = Service.objects.filter(pk=id, organization=org)

    if not service.exists():
        return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    service_name = request.data.get('service_name', '')
    service_description = request.data.get('service_description', '')
    
    service_obj = service[0]
    service_obj.service_name = service_name
    service_obj.service_description = service_description
    try:
        service_obj.full_clean()  # Validate the model instance
        service_obj.save()
        return Response({"message": "service edited successfully"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def delete_service(request, id):
    org = request.org
    service = Service.objects.filter(pk=id, organization=org)

    if not service.exists():
        return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    service[0].delete()
    return Response({"message": "The service does not exist"}, status=status.HTTP_200_OK)