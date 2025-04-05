from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.job_template_material import JobTemplateMaterial
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.material import Material
from django.core.exceptions import ValidationError

@api_view(["GET"])
def get_job_template_material_table_data(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user.pk)

    try:
        job_template = JobTemplate.objects.get(organization=org.pk, id=id)
    except JobTemplate.DoesNotExist:
        return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)

    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset', 0)
    
    if not pagesize or not offset:
        return Response({"message": "missing pagesize or offset"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pagesize = int(pagesize)
        offset = int(offset)
    except:
        return Response({"message": "pagesize and offset must be int"}, status=status.HTTP_400_BAD_REQUEST)
    
    job_template_materials = JobTemplateMaterial.objects.filter(job_template=job_template.pk)[offset:offset + pagesize]

    data = []
    for job_template_material in job_template_materials:
        data.append(job_template_material.json())
    
    count = JobTemplateMaterial.objects.filter(job_template=job_template.pk).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_job_template_material(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user)

    try:
        job_template_object = JobTemplate.objects.get(organization=org.pk, id=id)
    except:
        return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    materials_list = request.data.get('materials')

    if (len(materials_list) != 0):
        for material in materials_list:
            try:
                material_object = Material.objects.get(organization=org.pk, id=material["id"])
            except:
                return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            job_template_material_object = JobTemplateMaterial.objects.filter(job_template=job_template_object.pk, material=material_object.pk)

            if job_template_material_object.exists():
                return Response({"message": "The material for this job template already in the list"}, status=status.HTTP_400_BAD_REQUEST)

            job_template_material = JobTemplateMaterial(
                job_template = job_template_object,
                material = material_object,
                units_used = material['unitsUsed'],
                price_per_unit = material['pricePerUnit']
            )

            try:
                job_template_material.full_clean()  # Validate the model instance
                job_template_material.save()
                
            except ValidationError as e:
                return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Materials added to job template successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "There is no material to add"}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(["POST"])
def delete_job_template_material(request, job_template_id, job_template_material_id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    job_template_material = JobTemplateMaterial.objects.filter(pk=job_template_material_id, job_template=job_template_id)

    if not job_template_material.exists():
        return Response({"message": "The material in this job template does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    job_template_material[0].delete()
    return Response({"message": "The material in this job template deleted sucessfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def delete_cached_job_template_material(request, job_template_id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    job_template_materials_list = request.data.get('jobTemplateMaterials', '')      # dataform: jobTemplateMaterials: [{"id": int}, {"id": int}, ...]

    if (len(job_template_materials_list) != 0):
        for job_template_material in job_template_materials_list:
            try:
                job_template_material_object = JobTemplateMaterial.objects.get(id=job_template_material["id"])
            except:
                return Response({"message": "The material in this job template does not exist"}, status=status.HTTP_404_NOT_FOUND)

            job_template_material_object.delete()
    else:
        return Response({"message": "There is no material to delete"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "The materials in this job template deleted sucessfully"}, status=status.HTTP_200_OK)