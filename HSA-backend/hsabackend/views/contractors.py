from rest_framework.decorators import api_view
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_table_data, delete_object, update_individual_data, create_individual_data


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_contractor_table_data(request):
    return get_table_data(request, 'contractor')

@api_view(["GET"])
@check_authenticated_and_onboarded(require_onboarding=False)
def get_contractor_excluded_table_data(request):
    return get_table_data(request, 'contractor', exclude=True)
    
@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def create_contractor(request):
    return create_individual_data(request, "contractor")
@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_contractor(request, contractor_id):
    return update_individual_data(request, contractor_id, "contractor")
@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def delete_contractor(request, contractor_id):
    return delete_object(request, contractor_id, "contractor")