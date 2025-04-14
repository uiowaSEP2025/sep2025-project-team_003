from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.material import Material
from django.db.models import Q
from django.core.exceptions import ValidationError
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded 

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_material_table_data(request):
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
    materials = Material.objects.filter(organization=org.pk).filter(
        Q(material_name__icontains=search)
    )[offset:offset + pagesize] if search else Material.objects.filter(organization=org.pk)[offset:offset + pagesize]
 
    data = []
    for material in materials:
        data.append(material.json())
    
    count = Material.objects.filter(organization=org.pk).filter(
        Q(material_name__icontains=search)
    ).count()
 
    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["GET"])
@check_authenticated_and_onboarded(require_onboarding=False)
def get_material_excluded_table_data(request):
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
    materials = Material.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).filter(
        Q(material_name__icontains=search)
    )[offset:offset + pagesize] if search else Material.objects.filter(organization=org.pk).exclude(id__in=excluded_ids)[offset:offset + pagesize]
 
    data = []
    for material in materials:
        data.append(material.json())
    
    count = Material.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).filter(
        Q(material_name__icontains=search)
    ).count() if search else Material.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).count()
 
    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)
 
@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def create_material(request):
    org = request.org
    material_name = request.data.get('material_name', '')
    material_description = request.data.get('material_description', '')
    material_default_cost = request.data.get('default_cost', 0)
 
    material = Material(
        material_name = material_name,
        organization = org,
        material_description = material_description,
        default_cost = material_default_cost,
    )
 
    try:
        material.full_clean()
        material.save()
        return Response({"message": "Material created successfully", "data": material.json()}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_material(request, id):
    org = request.org
    try:
        material = Material.objects.get(pk=id, organization=org)
    except Material.DoesNotExist:
        return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)
 
    if not material:
        return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)

    material_name = request.data.get('material_name', '')
    material_description = request.data.get('material_description', '')
    material_default_cost = request.data.get('default_cost', 0)

    material.material_name = material_name
    material.material_description = material_description
    material.default_cost = material_default_cost
    
    try:
        material.full_clean()  # Validate the model instance
        material.save()
        return Response({"message": "material edited successfully"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    
 
@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def delete_material(request, id):
    org = request.org
    material = Material.objects.filter(pk=id, organization=org)
 
    if not material.exists():
        return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    material[0].delete()
 
    return Response({"message": "The material was deleted"}, status=status.HTTP_200_OK)