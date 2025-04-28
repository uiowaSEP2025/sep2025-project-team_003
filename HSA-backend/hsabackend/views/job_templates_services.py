from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.service import Service
from django.db.models import Q
from django.core.exceptions import ValidationError
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_template_service_table_data(request, id):
    org = request.organization

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
    
    job_template_services = JobTemplateService.objects.filter(job_template=job_template.pk)[offset:offset + pagesize]

    data = []
    for job_template_service in job_template_services:
        data.append(job_template_service.json())
    
    count = JobTemplateService.objects.filter(job_template=job_template.pk).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def create_job_template_service(request, id):
    org = request.organization

    try:
        job_template_object = JobTemplate.objects.get(organization=org.pk, id=id)
    except:
        return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    services_list = request.data.get('services', '')
    
    if (len(services_list) != 0):
        for service in services_list:
            try:
                service_object = Service.objects.get(organization=org.pk, id=service["id"])
            except:
                return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            job_template_service_object = JobTemplateService.objects.filter(job_template=job_template_object.pk, service=service_object.pk)

            if job_template_service_object.exists():
                return Response({"message": "The service for this job template already in the list"}, status=status.HTTP_400_BAD_REQUEST)

            job_template_service = JobTemplateService(
                job_template = job_template_object,
                service = service_object,
            )

            try:
                job_template_service.full_clean()  # Validate the model instance
                job_template_service.save()
            except ValidationError as e:
                return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"message": "Services added to job template successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "There is no service to add"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_job_template_service(request, job_template_id, job_template_service_id):
    
    job_template_service = JobTemplateService.objects.filter(pk=job_template_service_id, job_template=job_template_id)

    if not job_template_service.exists():
        return Response({"message": "The service in this job template does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    job_template_service[0].delete()
    return Response({"message": "The service in this job template deleted sucessfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_cached_job_template_service(request, job_template_id):
    job_template_services_list = request.data.get('jobTemplateServices', '')      # dataform: jobTemplateServices: [{"id": int}, {"id": int}, ...]

    if (len(job_template_services_list) != 0):
        for job_template_service in job_template_services_list:
            try:
                job_template_service_object = JobTemplateService.objects.get(id=job_template_service["id"])
            except:
                return Response({"message": "The service in this job template does not exist"}, status=status.HTTP_404_NOT_FOUND)

            job_template_service_object.delete()
    else:
        return Response({"message": "There is no service to delete"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "The services in this job template deleted sucessfully"}, status=status.HTTP_200_OK)