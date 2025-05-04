from rest_framework.decorators import api_view
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_table_data, delete_object, update_individual_data, \
    create_individual_data


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_discounts(request):
    return get_table_data(request, "discount")

@api_view(["POST"])
@check_authenticated_and_onboarded()
def create_discount(request):
    return create_individual_data(request, "discount")
@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_discount(request, discount_id):
    return update_individual_data(request, discount_id, "discount")

@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_discount(request, discount_id):
    return delete_object(request, discount_id, "discount")