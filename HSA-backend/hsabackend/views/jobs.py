from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.contractor import Contractor
from hsabackend.models.job import Job
from hsabackend.models.material import Material
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.serializers.job_contractor_serializer import JobContractorSerializer
from hsabackend.serializers.job_material_serializer import JobMaterialSerializer
from hsabackend.serializers.job_serializer import JobSerializer
from hsabackend.serializers.job_service_serializer import JobServiceSerializer


@api_view(["GET"])
def get_job_table_data(request):
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
    jobs = Job.objects.filter(organization=org.pk).filter(
        Q(customer__first_name__icontains=search) | 
        Q(customer__last_name__icontains=search) | 
        Q(start_date__icontains=search) | 
        Q(end_date__icontains=search) |
        Q(job_status__icontains=search) |
        Q(description__icontains=search)
    )[offset:offset + pagesize] if search else Job.objects.filter(organization=org.pk)[offset:offset + pagesize]

    serializer = JobSerializer(jobs, many=True)

    count = Job.objects.filter(organization=org.pk).filter(
        Q(customer__first_name__icontains=search) | 
        Q(customer__last_name__icontains=search) | 
        Q(start_date__icontains=search) | 
        Q(end_date__icontains=search) |
        Q(job_status__icontains=search) |
        Q(description__icontains=search)
    ).count()

    res = {
        'data': serializer.data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_job_individual_data(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    org = Organization.objects.get(owning_User=request.user.pk)

    try:
        job = Job.objects.get(pk=id, organization=org)
    except Job.DoesNotExist:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if not job:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)



    job_serializer = JobSerializer(job)
    job_services_serializer = JobServiceSerializer(job, many=True)
    job_materials_serializer = JobMaterialSerializer(job, many=True)
    job_contractors_serializer = JobContractorSerializer(job, many=True)

    res = {
        'data': job_serializer.data,
        'services': {'services': job_services_serializer.data},
        'materials': {'materials': job_materials_serializer.data},
        'contractors': {'contractors': job_contractors_serializer.data}
    }    

    return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_job(request):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    org = Organization.objects.get(owning_User=request.user)

    # Prepare job data
    job_data = {
        'job_status': "created",
        'start_date': request.data.get('startDate', ''),
        'end_date': request.data.get('endDate', ''),
        'description': request.data.get('description', ''),
        'organization': org.pk,
        'customer': request.data.get('customerID'),
        'requestor_address': request.data.get('address', ''),
        'requestor_city': request.data.get('city', ''),
        'requestor_state': request.data.get('state', ''),
        'requestor_zip': request.data.get('zip', '')
    }

    # Create and validate job
    job_serializer = JobSerializer(data=job_data)
    if not job_serializer.is_valid():
        return Response({"errors": job_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    job = job_serializer.save()

    # Process services
    service_list = request.data.get('services', '')
    for service in service_list:
        try:
            service_object = Service.objects.get(organization=org.pk, id=service["id"])

            service_data = {
                'job': job.pk,
                'service': service_object.pk
            }

            job_service_serializer = JobServiceSerializer(data=service_data)
            if job_service_serializer.is_valid():
                job_service_serializer.save()
            else:
                return Response({"errors": job_service_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Service.DoesNotExist:
            return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Process materials
    material_list = request.data.get('materials', '')
    for material in material_list:
        try:
            material_object = Material.objects.get(organization=org.pk, id=material["id"])

            material_data = {
                'job': job.pk,
                'material': material_object.pk,
                'units_used': material["unitsUsed"],
                'price_per_unit': material["pricePerUnit"]
            }

            job_material_serializer = JobMaterialSerializer(data=material_data)
            if job_material_serializer.is_valid():
                job_material_serializer.save()
            else:
                return Response({"errors": job_material_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Material.DoesNotExist:
            return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Process contractors
    contractor_list = request.data.get('contractors', '')
    for contractor in contractor_list:
        try:
            contractor_object = Contractor.objects.get(organization=org.pk, id=contractor["id"])

            contractor_data = {
                'job': job.pk,
                'contractor': contractor_object.pk
            }

            job_contractor_serializer = JobContractorSerializer(data=contractor_data)
            if job_contractor_serializer.is_valid():
                job_contractor_serializer.save()
            else:
                return Response({"errors": job_contractor_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Contractor.DoesNotExist:
            return Response({"message": "The contractor does not exist"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"message": "Job created successfully"}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def edit_job(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    org = Organization.objects.get(owning_User=request.user)

    try:
        job = Job.objects.get(pk=id, organization=org)
    except Job.DoesNotExist:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if not job:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Prepare job data
    job_data = {
        'job_status': request.data.get('jobStatus', ''),
        'start_date': request.data.get('startDate', ''),
        'end_date': request.data.get('endDate', ''),
        'description': request.data.get('description', ''),
        'organization': org.pk,
        'customer': request.data.get('customerID'),
        'requestor_address': request.data.get('address', ''),
        'requestor_city': request.data.get('city', ''),
        'requestor_state': request.data.get('state', ''),
        'requestor_zip': request.data.get('zip', '')
    }

    # Update and validate job
    job_serializer = JobSerializer(job, data=job_data, partial=True)
    if job_serializer.is_valid():
        job_serializer.save()
        return Response({"message": "Job edited successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"errors": job_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delete_job(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    org = Organization.objects.get(owning_User=request.user)
    job = Job.objects.filter(pk=id, organization=org)

    if not job.exists():
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)

    job[0].delete()
    return Response({"message": "Job deleted sucessfully"}, status=status.HTTP_200_OK)
