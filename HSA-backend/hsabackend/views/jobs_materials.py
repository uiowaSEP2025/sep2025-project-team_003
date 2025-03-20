from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.job_material import JobMaterial
from hsabackend.models.job import Job
from hsabackend.models.material import Material
from django.db.models import Q
from django.core.exceptions import ValidationError

@api_view(["GET"])
def get_job_material_table_data(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user.pk)

    try:
        job = Job.objects.get(organization=org.pk, id=id)
    except Job.DoesNotExist:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)

    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset', 0)
    
    if not pagesize or not offset:
        return Response({"message": "missing pagesize or offset"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pagesize = int(pagesize)
        offset = int(offset)
    except:
        return Response({"message": "pagesize and offset must be int"}, status=status.HTTP_400_BAD_REQUEST)
    
    job_materials = JobMaterial.objects.filter(job=job.pk)[offset:offset + pagesize]

    data = []
    for job_material in job_materials:
        data.append(job_material.json())
    
    count = JobMaterial.objects.filter(job=job.pk).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_job_material(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user)

    try:
        job_object = Job.objects.get(organization=org.pk, id=id)
    except:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    materials_list = request.data.get('materials')

    if (len(materials_list) != 0):
        for material in materials_list:
            try:
                material_object = Material.objects.get(organization=org.pk, id=material["id"])
            except:
                return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            job_material_object = JobMaterial.objects.filter(job=job_object.pk, material=material_object.pk)

            if job_material_object.exists():
                return Response({"message": "The material for this job already in the list"}, status=status.HTTP_400_BAD_REQUEST)

            job_material = JobMaterial(
                job = job_object,
                material = material_object,
                units_used = material['unitsUsed'],
                price_per_unit = material['pricePerUnit']
            )

            try:
                job_material.full_clean()  # Validate the model instance
                job_material.save()
                
            except ValidationError as e:
                return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Materials added to job successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "There is no material to add"}, status=status.HTTP_400_BAD_REQUEST)


    
    
@api_view(["POST"])
def delete_job_material(request, job_id, job_material_id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    job_material = JobMaterial.objects.filter(pk=job_material_id, job=job_id)

    if not job_material.exists():
        return Response({"message": "The material in this job does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    job_material[0].delete()
    return Response({"message": "The material in this job deleted sucessfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def delete_cached_job_material(request, job_id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    job_materials_list = request.data.get('job_materials', '')      # dataform: job_materials: [{"id": int}, {"id": int}, ...]

    if (len(job_materials_list) != 0):
        for job_material in job_materials_list:
            try:
                job_material_object = JobMaterial.objects.get(id=job_material["id"])
            except:
                return Response({"message": "The material in this job does not exist"}, status=status.HTTP_404_NOT_FOUND)

            job_material_object.delete()
    else:
        return Response({"message": "There is no material to delete"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "The materials in this job deleted sucessfully"}, status=status.HTTP_200_OK)