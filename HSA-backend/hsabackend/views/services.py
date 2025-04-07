from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from django.db.models import Q
from django.core.exceptions import ValidationError

@api_view(["GET"])
def get_service_table_data(request):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user.pk)
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
def get_service_excluded_table_data(request):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user.pk)
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
def create_service(request):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user)
    service_name = request.data.get('service_name', '')
    service_description = request.data.get('service_description', '')
    service_default_hourly_rate = request.data.get('default_hourly_rate', 0.00)

    service = Service(
        service_name = service_name,
        service_description = service_description,
        organization = org,
        default_hourly_rate = service_default_hourly_rate,
    )

    try:
        service.full_clean()  # Validate the model instance
        service.save()
        return Response({"message": "service created successfully"}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"errors": e.error_list}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def edit_service(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user)
    service = Service.objects.get(pk=id)

    if not service.DoesNotExist:
        return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    service_name = request.data.get('service_name', '')
    service_description = request.data.get('service_description', '')
    service_default_hourly_rate = request.data.get('default_hourly_rate', 0)
    service.service_name = service_name
    service.service_description = service_description
    service.organization = org
    service.default_hourly_rate = service_default_hourly_rate
    try:
        service.full_clean()  # Validate the model instance
        service.save()
        return Response({"message": "service edited successfully"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def delete_service(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user)
    service = Service.objects.filter(pk=id, organization=org)

    if not service.exists():
        return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    service[0].delete()
    return Response({"message": "The service does not exist"}, status=status.HTTP_200_OK)