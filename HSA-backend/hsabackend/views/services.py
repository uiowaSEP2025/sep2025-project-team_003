from rest_framework.decorators import api_view

from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_table_data, create_individual_data, update_individual_data, \
    delete_object


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_service_table_data(request):
    return get_table_data(request, "service")

@api_view(["GET"])
@check_authenticated_and_onboarded(require_onboarding=False)
def get_service_excluded_table_data(request):
    return get_table_data(request, "service", exclude=True)

@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def create_service(request):
    return create_individual_data(request, "service")

@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_service(request, service_id):
    return update_individual_data(request, service_id, "service")
@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def delete_service(request, service_id):
    return delete_object(request, service_id, "service")