from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.job import Job
from hsabackend.models.contractor import Contractor
from django.db.models import Q
from django.core.exceptions import ValidationError

@api_view(["GET"])
def get_job_contractor_table_data(request, id):
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
    
    job_contractors = JobContractor.objects.filter(job=job.pk)[offset:offset + pagesize]

    data = []
    for job_contractor in job_contractors:
        data.append(job_contractor.json())
    
    count = JobContractor.objects.filter(job=job.pk).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_job_contractor(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user)

    try:
        job_object = Job.objects.get(organization=org.pk, id=id)
    except:
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    contractors_list = request.data.get('contractors', '')

    if (len(contractors_list) != 0):
        for contractor in contractors_list:
            try:
                contractor_object = Contractor.objects.get(organization=org.pk, id=contractor["id"])
            except:
                return Response({"message": "The contractor does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            job_contractor_object = JobContractor.objects.filter(job=job_object.pk, contractor=contractor_object.pk)

            if job_contractor_object.exists():
                return Response({"message": "The contractor for this job already in the list"}, status=status.HTTP_400_BAD_REQUEST)

            job_contractor = JobContractor(
                job = job_object,
                contractor = contractor_object,
            )

            try:
                job_contractor.full_clean()  # Validate the model instance
                job_contractor.save()
            except ValidationError as e:
                return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"message": "Contractors added to job successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "There is no contractor to add"}, status=status.HTTP_400_BAD_REQUEST)
            
@api_view(["POST"])
def delete_job_contractor(request, job_id, job_contractor_id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    job_contractor = JobContractor.objects.filter(pk=job_contractor_id, job=job_id)

    if not job_contractor.exists():
        return Response({"message": "The contractor in this job does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    job_contractor[0].delete()
    return Response({"message": "The contractor in this job deleted sucessfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def delete_cached_job_contractor(request, job_id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    job_contractors_list = request.data.get('jobContractors', '')      # dataform: jobContractors: [{"id": int}, {"id": int}, ...]

    if (len(job_contractors_list) != 0):
        for job_contractor in job_contractors_list:
            try:
                job_contractor_object = JobContractor.objects.get(id=job_contractor["id"])
            except:
                return Response({"message": "The contractor in this job does not exist"}, status=status.HTTP_404_NOT_FOUND)

            job_contractor_object.delete()
    else:
        return Response({"message": "There is no contractor to delete"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "The contractors in this job deleted sucessfully"}, status=status.HTTP_200_OK)