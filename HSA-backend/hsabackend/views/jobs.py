from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.customer import Customer
from hsabackend.models.job import Job
from hsabackend.serializers.job_contractor_serializer import JobContractorSerializer
from hsabackend.serializers.job_material_serializer import JobMaterialSerializer
from hsabackend.serializers.job_serializer import JobSerializer
from hsabackend.serializers.job_service_serializer import JobServiceSerializer
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from utils.response_helpers import get_table_data


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_table_data(request):

    return get_table_data(request, "job")


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_excluded_table_data(request):
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
    jobs = Job.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).filter(
        Q(customer__first_name__icontains=search) |
        Q(customer__last_name__icontains=search) |
        Q(start_date__icontains=search) |
        Q(end_date__icontains=search) |
        Q(job_status__icontains=search) |
        Q(description__icontains=search)
    )[offset:offset + pagesize] if search else Job.objects.filter(organization=org.pk).exclude(id__in=excluded_ids)[offset:offset + pagesize]

    data = []
    for job in jobs:
        data.append(job.json_simplify())

    count = Job.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).filter(
        Q(customer__first_name__icontains=search) |
        Q(customer__last_name__icontains=search) |
        Q(start_date__icontains=search) |
        Q(end_date__icontains=search) |
        Q(job_status__icontains=search) |
        Q(description__icontains=search)
    ).count() if search else Job.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).count()

    serializer = JobSerializer(jobs, many=True)
    res = {
        'data': serializer.data,
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
@check_authenticated_and_onboarded(require_onboarding=False)
def create_job(request):
    org = request.org

    customer = Customer.objects.filter(organization=org.pk).filter(id=request.data.get('customerID')).first()

    # Prepare job data
    job_data = {
        'job_status': "created",
        'start_date': request.data.get('startDate', ''),
        'end_date': request.data.get('endDate', ''),
        'description': request.data.get('description', ''),
        'organization': org,
        'customer': customer,
        'services': request.data.get('services', []),
        'materials': request.data.get('materials', []),
        'contractors': request.data.get('contractors', []),
        'job_address': request.data.get('address', ''),
        'job_city': request.data.get('city', ''),
        'job_state': request.data.get('state', ''),
        'job_zip': request.data.get('zip', ''),
        'use_hourly_rate': request.data.get('useHourlyRate', False),
        'minutes_worked': request.data.get('minutesWorked', 0),
        'hourly_rate': request.data.get('hourlyRate', 0),
    }

    # Create and validate a job
    job_serializer = JobSerializer(data=job_data)
    if not job_serializer.is_valid():
        return Response({"errors": job_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    job_serializer.create(job_data)

    return Response({"message": "Job created successfully"}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_job(request, job_id):


    org = request.org

    try:
        job = Job.objects.get(pk=job_id, organization=org)
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
        'job_address': request.data.get('address', ''),
        'job_city': request.data.get('city', ''),
        'job_state': request.data.get('state', ''),
        'job_zip': request.data.get('zip', ''),
        'invoice': request.data.get('invoice', ''),
        'use_hourly_rate': request.data.get('useHourlyRate', False),
        'minutes_worked': request.data.get('minutesWorked', 0),
        'hourly_rate': request.data.get('hourlyRate', 0),
        'services': request.data.get('services', []),
        'materials': request.data.get('materials', []),
        'contractors': request.data.get('contractors', []),
    }

    # Update and validate the job
    job_serializer = JobSerializer(job, data=job_data)
    if job_serializer.is_valid():
        job_serializer.update(job, job_data)
        return Response({"message": "Job edited successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"errors": job_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_job(request, job_id):


    org = request.org
    job = Job.objects.filter(pk=job_id, organization=org)

    if not job.exists():
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)

    job[0].delete()
    return Response({"message": "Job deleted successfully"}, status=status.HTTP_200_OK)
