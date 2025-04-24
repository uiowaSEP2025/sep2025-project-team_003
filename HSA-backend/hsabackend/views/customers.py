from rest_framework.decorators import api_view

from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_table_data, create_individual_data, update_individual_data, \
    delete_object


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_customer_table_data(request):
    return get_table_data(request, 'customer')

@api_view(["GET"])
@check_authenticated_and_onboarded(require_onboarding=False)
def get_customer_excluded_table_data(request):
    return get_table_data(request, 'customer', exclude=True)
    
@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def create_customer(request):
    return create_individual_data(request,"customer")

@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_customer(request, customer_id):
    return update_individual_data(request, customer_id, "customer")
@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def delete_customer(request, customer_id):
    delete_object(request, customer_id, "customer")