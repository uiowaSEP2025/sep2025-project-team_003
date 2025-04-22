from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.job import Job
from hsabackend.models.service import Service
from django.db.models import Q
from django.core.exceptions import ValidationError
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_service_table_data(request, id):
    org = request.org

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
    
    job_services = JobService.objects.filter(job=job.pk)[offset:offset + pagesize]

    data = []
    for job_service in job_services:
        data.append(job_service.json())
    
    count = JobService.objects.filter(job=job.pk).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def create_job_service(request, id):
    org = request.org

    try:
        job_object = Job.objects.get(organization=org.pk, id=id)
    except:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    services_list = request.data.get('services', '')
    
    if (len(services_list) != 0):
        for service in services_list:
            try:
                service_object = Service.objects.get(organization=org.pk, id=service["id"])
            except:
                return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            job_service_object = JobService.objects.filter(job=job_object.pk, service=service_object.pk)

            if job_service_object.exists():
                return Response({"message": "The service for this job already in the list"}, status=status.HTTP_400_BAD_REQUEST)

            job_service = JobService(
                job = job_object,
                service = service_object,
            )

            try:
                job_service.full_clean()  # Validate the model instance
                job_service.save()
            except ValidationError as e:
                return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"message": "Services added to job successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "There is no service to add"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_job_service(request, job_id, job_service_id):
    job_service = JobService.objects.filter(pk=job_service_id, job=job_id)

    if not job_service.exists():
        return Response({"message": "The service in this Job does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    job_service[0].delete()
    return Response({"message": "The service in this job deleted sucessfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_cached_job_service(request, job_id):
    job_services_list = request.data.get('jobServices', '')      # dataform: jobServices: [{"id": int}, {"id": int}, ...]

    if (len(job_services_list) != 0):
        for job_service in job_services_list:
            try:
                job_service_object = JobService.objects.get(id=job_service["id"])
            except:
                return Response({"message": "The service in this job does not exist"}, status=status.HTTP_404_NOT_FOUND)

            job_service_object.delete()
    else:
        return Response({"message": "There is no service to delete"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "The services in this job deleted sucessfully"}, status=status.HTTP_200_OK)