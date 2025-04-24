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

from hsabackend.utils.response_helpers import get_individual_data, create_individual_data, update_individual_data


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_table_data(request):
    return get_table_data(request, "job")


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_excluded_table_data(request):
    return get_table_data(request, "job", exclude=True)

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_individual_data(request, job_id):
    return get_individual_data(request, job_id, "job")

@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def create_job(request):
    return create_individual_data(request, "job")
@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_job(request, job_id):
    return update_individual_data(request, job_id, "job")

@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_job(request, job_id):


    org = request.org
    job = Job.objects.filter(pk=job_id, organization=org)

    if not job.exists():
        return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)

    job[0].delete()
    return Response({"message": "Job deleted successfully"}, status=status.HTTP_200_OK)
