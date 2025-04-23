from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.job_template import JobTemplate
from hsabackend.models.material import Material
from hsabackend.models.service import Service
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from utils.response_helpers import get_table_data


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_template_table_data(request):

    return get_table_data(request, "job_template")


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_template_individual_data(request, id):
    org = request.org
    
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

    # DO NOT TOUCH OR IT WILL BREAK!, YES ITS BAD, WE KNOW!
    res = {
        'data': job_template.json(),
        'services': {'services': job_template_services_data},
        'materials': {'materials': job_template_materials_data},
    }    

    return Response(res, status=status.HTTP_200_OK)


@api_view(["POST"])
@check_authenticated_and_onboarded()
def create_job_template(request):
    org = request.org
    
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
@check_authenticated_and_onboarded()
def edit_job_template(request, id):
    org = request.org

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
@check_authenticated_and_onboarded()
def delete_job_template(request, id):
    org = request.org
    job_template = JobTemplate.objects.filter(pk=id, organization=org)

    if not job_template.exists():
        return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    job_template[0].delete()
    return Response({"message": "Job template deleted sucessfully"}, status=status.HTTP_200_OK)