from rest_framework.decorators import api_view

from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_individual_data, create_individual_data, update_individual_data, \
    delete_object
from hsabackend.utils.response_helpers import get_table_data


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