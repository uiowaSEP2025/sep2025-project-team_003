from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from hsabackend.controller.job_serializer import JobSerializer
from hsabackend.models.organization import Organization
from hsabackend.models.customer import Customer
from hsabackend.models.job import Job, JobsServices, JobsMaterials
from hsabackend.models.service import Service
from hsabackend.models.material import Material
from hsabackend.models.contractor import Contractor
from django.db.models import Q
from django.core.exceptions import ValidationError
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_table_data(request):
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
@check_authenticated_and_onboarded()
def get_job_individual_data(request, id):
    org = request.org
    
    try:
        job = Job.objects.get(pk=id, organization=org)
    except Job.DoesNotExist:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)
 
    if not job:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)

    serializer = JobSerializer(job)


    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def create_job(request):
    org = request.org
    job_description = request.data.get('description', '')
    job_start_date = request.data.get('startDate', '')
    job_end_date = request.data.get('endDate', '')
    customer = Customer.objects.get(id=request.data.get('customerID'))
    job_city = request.data.get('city', '')
    job_state = request.data.get('state', '')
    job_zip = request.data.get('zip', '')
    job_address = request.data.get('address', '')

    contractor_list = request.data.get('contractors', '')   # data send form: contractors: [{ "id": int }]
    service_list = request.data.get('services', '')         # data send form: services: [{ "id": int }]
    material_list = request.data.get('materials', '')       # data send form: materials: [{ "id": int, "unitsUsed": int, "pricePerUnit": float }]
    
    # Initialize job entry first
    job = Job(
        job_status = "created",
        start_date = job_start_date,
        end_date = job_end_date,
        description = job_description,
        organization = org,
        customer = customer,
        job_address = job_address,
        job_city = job_city,
        job_state = job_state,
        job_zip = job_zip
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

            if service_object:
                job_service = JobsServices(
                    job = job,
                    service = service_object
                )
                try:
                    job_service.full_clean()
                    job_service.save()
                except ValidationError as e:
                    return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
        except Service.DoesNotExist:
            return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)


    # Add material and job join entry
    for material in material_list:
        try:
            material_object = Material.objects.get(organization=org.pk, id=material["id"])
            if material_object:
                job_material = JobsMaterials(
                    job = job,
                    material = material_object,
                )
                try:
                    job_material.full_clean()
                    job_material.save()
                except ValidationError as e:
                    return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
        except Material.DoesNotExist:
            return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)


    # Add contractor and job join entry
    for contractor in contractor_list:
        try:
            contractor_object = Contractor.objects.get(organization=org.pk, id=contractor["id"])

            job.contractors.add(contractor_object)
        except Contractor.DoesNotExist:
            return Response({"message": "The contractor does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            job.full_clean()
            job.save()
        except ValidationError as e:
            return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)      
          
    return Response({"message": "Job created successfully"}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_job(request, id):
    org = request.org

    try:
        job = Job.objects.get(pk=id, organization=org)
    except Job.DoesNotExist:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)
 
    if not job:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)


    job.job_status = request.data.get('jobStatus','')
    job.start_date = request.data.get('startDate','')
    job.end_date = request.data.get('endDate','')
    job.services = request.data.get('services','')
    job.materials = request.data.get('materials','')
    job.description = request.data.get('description','')
    job.job_address = request.data.get('address','')
    job.job_city = request.data.get('city','')
    job.job_state = request.data.get('state','')
    job.job_zip = request.data.get('zip','')

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
@check_authenticated_and_onboarded()
def delete_job(request, id):
    org = request.org
    job = Job.objects.filter(pk=id, organization=org)

    if not job.exists():
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    job[0].delete()
    return Response({"message": "Job deleted sucessfully"}, status=status.HTTP_200_OK)