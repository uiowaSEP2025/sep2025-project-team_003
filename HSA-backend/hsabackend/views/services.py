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