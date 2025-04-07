from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from django.db.models import Q
from django.core.exceptions import ValidationError
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.job_template_service import JobTemplateService
from hsabackend.models.job_template_material import JobTemplateMaterial
from hsabackend.models.service import Service
from hsabackend.models.material import Material

@api_view(["GET"])
def get_job_template_table_data(request):
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
    job_templates = JobTemplate.objects.filter(organization=org.pk).filter(
        Q(name__icontains=search) |
        Q(description__icontains=search)
    )[offset:offset + pagesize] if search else JobTemplate.objects.filter(organization=org.pk)[offset:offset + pagesize]

    data = []
    for job in job_templates:
        data.append(job.json())
    
    count = JobTemplate.objects.filter(organization=org.pk).filter(
        Q(name__icontains=search) |
        Q(description__icontains=search)
    ).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_job_template_individual_data(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user.pk)
    
    try:
        job_template = JobTemplate.objects.get(pk=id, organization=org)
    except JobTemplate.DoesNotExist:
        return Response({"message": "The job_template does not exist"}, status=status.HTTP_404_NOT_FOUND)
 
    if not job_template:
        return Response({"message": "The job_template does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    
    job_template_services = JobTemplateService.objects.filter(job_template=job_template.pk)
    job_template_materials = JobTemplateMaterial.objects.filter(job_template=job_template.pk)

    job_template_services_data = []
    for service in job_template_services:
        job_template_services_data.append(service.json())
    
    job_template_materials_data = []
    for material in job_template_materials:
        job_template_materials_data.append(material.json())

    res = {
        'data': job_template.json(),
        'services': {'services': job_template_services_data},
        'materials': {'materials': job_template_materials_data},
    }    

    return Response(res, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_job_template(request):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        org = Organization.objects.get(owning_User=request.user)
    except Organization.DoesNotExist:
        return Response({"message": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
    
    job_name = request.data.get('name', '')
    job_description = request.data.get('description', '')
    service_list = request.data.get('services', [])
    material_list = request.data.get('materials', [])

    job_template = JobTemplate(
        description=job_description,
        name=job_name,
        organization=org
    )

    try:
        job_template.full_clean()
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    job_template.save()
    errors = []

    # Add service to job_template join
    for service in service_list:
        try:
            service_object = Service.objects.get(organization=org.pk, id=service["id"])
        except Service.DoesNotExist:
            errors.append({"service": f"Service does not exist"})
            continue

        job_template_service = JobTemplateService(
            job_template=job_template,
            service=service_object
        )

        try:
            job_template_service.full_clean()
            job_template_service.save()
        except ValidationError as e:
            errors.append({"service": e.message_dict})

    # Add material to job_template join
    for material in material_list:
        try:
            material_object = Material.objects.get(organization=org.pk, id=material["id"])
        except Material.DoesNotExist:
            errors.append({"material": f"Material does not exist"})
            continue

        material_job_template = JobTemplateMaterial(
            material=material_object,
            job_template=job_template,
            units_used=material["unitsUsed"],
            price_per_unit=material["pricePerUnit"]
        )

        try:
            material_job_template.full_clean()
            material_job_template.save()
        except ValidationError as e:
            errors.append({"material": e.message_dict})

    if errors:
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Job template created successfully"}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def edit_job_template(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user)

    try:
        job_template = JobTemplate.objects.get(pk=id, organization=org)
    except JobTemplate.DoesNotExist:
        return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)
 
    if not job_template:
        return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)

    job_template.description = request.data.get('description','')
    job_template.name = request.data.get('name', '')

    try:
        job_template.full_clean()
        job_template.save()
        return Response({"message": "Job template edited successfully"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
def delete_job_template(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user)
    job_template = JobTemplate.objects.filter(pk=id, organization=org)

    if not job_template.exists():
        return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    job_template[0].delete()
    return Response({"message": "Job template deleted sucessfully"}, status=status.HTTP_200_OK)