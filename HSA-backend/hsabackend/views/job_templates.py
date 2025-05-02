from rest_framework.decorators import api_view

from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_table_data, delete_object, update_individual_data, create_individual_data, \
    get_individual_data


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_template_table_data(request):
    return get_table_data(request, "job_template")


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_job_template_individual_data(request, job_template_id):
    return get_individual_data(request, job_template_id, "job_template")


@api_view(["POST"])
@check_authenticated_and_onboarded()
def create_job_template(request):
    return create_individual_data(request, "job_template" )

@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_job_template(request, job_template_id):
    return update_individual_data(request, job_template_id, "job_template")

@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_job_template(request, job_template_id):
    return delete_object(request, job_template_id, "job_template")