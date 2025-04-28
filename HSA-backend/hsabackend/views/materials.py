from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.material import Material
from django.db.models import Q
from django.core.exceptions import ValidationError
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_table_data, create_individual_data, update_individual_data, \
    delete_object


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_material_table_data(request):
    return get_table_data(request, "material")

@api_view(["GET"])
@check_authenticated_and_onboarded(require_onboarding=False)
def get_material_excluded_table_data(request):
    return get_table_data(request, "material", exclude=True)
 
@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def create_material(request):
    return create_individual_data(request, "material")
@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_material(request, material_id):
    return update_individual_data(request, material_id, "material")

@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def delete_material(request, material_id):
    return delete_object(request, material_id, "material")