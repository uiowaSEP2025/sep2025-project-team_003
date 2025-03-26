from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.customer import Customer
from hsabackend.models.job import Job
from hsabackend.models.service import Service
from hsabackend.models.material import Material
from hsabackend.models.contractor import Contractor
from hsabackend.models.job_material import JobMaterial
from hsabackend.models.job_service import JobService
from hsabackend.models.job_contractor import JobContractor
from django.db.models import Q
from django.core.exceptions import ValidationError

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

    data = []
    for job in jobs:
        data.append(job.json_simplify())
    
    count = Job.objects.filter(organization=org.pk).filter(
        Q(customer__first_name__icontains=search) | 
        Q(customer__last_name__icontains=search) | 
        Q(start_date__icontains=search) | 
        Q(end_date__icontains=search) |
        Q(job_status__icontains=search) |
        Q(description__icontains=search)
    ).count()

    res = {
        'data': data,
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
    
    
    job_services = JobService.objects.filter(job=job.pk)
    job_materials = JobMaterial.objects.filter(job=job.pk)
    job_contractors = JobContractor.objects.filter(job=job.pk)

    job_services_data = []
    for service in job_services:
        job_services_data.append(service.json())
    
    job_materials_data = []
    for material in job_materials:
        job_materials_data.append(material.json())
    
    job_contractors_data = []
    for contractor in job_contractors:
        job_contractors_data.append(contractor.json())

    res = {
        'data': job.json(),
        'services': {'services': job_services_data},
        'materials': {'materials': job_materials_data},
        'contractors': {'contractors': job_contractors_data}
    }    

    return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_job(request):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user)
    job_description = request.data.get('description', '')
    job_start_date = request.data.get('startDate', '')
    job_end_date = request.data.get('endDate', '')
    customer = Customer.objects.get(id=request.data.get('customerID'))
    requestor_city = request.data.get('city', '')
    requestor_state = request.data.get('state', '')
    requestor_zip = request.data.get('zip', '')
    requestor_address = request.data.get('address', '')

    contractor_list = request.data.get('contractors', '')   # data send form: contractors: [{ "id": int }]
    service_list = request.data.get('services', '')         # data send form: services: [{ "id": int }]
    material_list = request.data.get('materials', '')       # data send form: materials: [{ "id": int, "unit": int, "pricePerUnit": float }]
    
    # Initialize job entry first
    job = Job(
        job_status = "created",
        start_date = job_start_date,
        end_date = job_end_date,
        description = job_description,
        organization = org,
        customer = customer,
        requestor_address = requestor_address,
        requestor_city = requestor_city,
        requestor_state = requestor_state,
        requestor_zip = requestor_zip
    )

    try:
        job.full_clean()  # Validate the model instance
        job.save()   
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    
    # Add service and job join entry
    for service in service_list:
        try:
            service_object = Service.objects.get(organization=org.pk, id=service["id"])

            if (service_object):
                job_service = JobService(
                    job = job,
                    service = service_object
                )
        except Service.DoesNotExist:
            return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            job_service.full_clean()
            job_service.save()
        except ValidationError as e:
            return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    
    # Add material and job join entry
    for material in material_list:
        try:
            material_object = Material.objects.get(organization=org.pk, id=material["id"])

            if (material_object):
                material_job = JobMaterial(
                    material = material_object,
                    job = job,
                    units_used = material["unitsUsed"],
                    price_per_unit = material["pricePerUnit"]
                )
        except Material.DoesNotExist:
            return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            material_job.full_clean()
            material_job.save()
        except ValidationError as e:
            return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    
    # Add contractor and job join entry
    for contractor in contractor_list:
        try:
            contractor_object = Contractor.objects.get(organization=org.pk, id=contractor["id"])

            if (contractor_object):
                job_contractor = JobContractor(
                    job = job,
                    contractor = contractor_object
                )
        except Contractor.DoesNotExist:
            return Response({"message": "The contractor does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            job_contractor.full_clean()
            job_contractor.save()
        except ValidationError as e:
            return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)      
          
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

    job.job_status = request.data.get('jobStatus','')
    job.start_date = request.data.get('startDate','')
    job.end_date = request.data.get('endDate','')
    job.description = request.data.get('description','')
    job.requestor_address = request.data.get('address','')
    job.requestor_city = request.data.get('city','')
    job.requestor_state = request.data.get('state','')
    job.requestor_zip = request.data.get('zip','')   

    try:
        customer = Customer.objects.get(id=request.data.get('customerID'))
        job.customer = customer
    except Customer.DoesNotExist:
        return Response({"message": "The customer does not exist"}, status=status.HTTP_404_NOT_FOUND)

    try:
        job.full_clean()
        job.save()
        return Response({"message": "Job edited successfully"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
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