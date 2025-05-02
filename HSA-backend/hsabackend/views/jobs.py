from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.job import Job
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_table_data, get_individual_data, create_individual_data, \
    update_individual_data, delete_object


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_jobs_by_contractor(request):
    org = request.org
    search = request.query_params.get('search', '')
    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset', 0)
    contractor_id = request.query_params.get('contractor', 0)

    if not pagesize or not offset:
        return Response({"message": "missing pagesize or offset"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pagesize = int(pagesize)
        offset = int(offset)
        contractor_id = int(contractor_id)
    except:
        return Response({"message": "pagesize, offset, and contractor_id must be int"}, status=status.HTTP_400_BAD_REQUEST)

    jobs = Job.objects.filter(
        organization=org.pk,
        jobcontractor__contractor__id=contractor_id
    ).filter(
        Q(customer__first_name__icontains=search) |
        Q(customer__last_name__icontains=search) |
        Q(start_date__icontains=search) |
        Q(end_date__icontains=search) |
        Q(job_status__icontains=search) |
        Q(description__icontains=search)
    ).distinct()

    jres = []

    for job in jobs:
        jres.append(job.json_simplify())

    count = Job.objects.filter(
        organization=org.pk,
        jobcontractor__contractor__id=contractor_id
    ).filter(
        Q(customer__first_name__icontains=search) |
        Q(customer__last_name__icontains=search) |
        Q(start_date__icontains=search) |
        Q(end_date__icontains=search) |
        Q(job_status__icontains=search) |
        Q(description__icontains=search)
    ).count()

    jres = []

    for j in jobs:
        jres.append(j.json_simplify())

    res = {
        'data': jres,
        'totalCount': count
    }

    return Response(res, status=status.HTTP_200_OK)


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
    return delete_object(request, job_id, "job")