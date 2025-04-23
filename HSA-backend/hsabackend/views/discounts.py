from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.discount import Discount
from hsabackend.serializers.discount_serializer import DiscountSerializer
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from utils.response_helpers import get_table_data


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_discounts(request):
    return get_table_data(request, "discount")

@api_view(["POST"])
@check_authenticated_and_onboarded()
def create_discount(request):
    org = request.org
    discount_name = request.data.get('name', '')
    discount_percent = request.data.get('percent', '')

    discount_data = {
        'discount_name': discount_name,
        'discount_percent': discount_percent,
        'organization': org,
    }

    serializer = DiscountSerializer(data=discount_data)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.create(discount_data)
        return Response({"message": "discount created"}, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_discount(request, discount_id):
    org = request.org
    discount_name = request.data.get('name', '')
    discount_percent = request.data.get('percent', '')
    discount = Discount.objects.filter(pk=discount_id, organization=org)
    if not discount.exists():
        return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
    discount_data = {
        'discount_name': discount_name,
        'discount_percent': discount_percent,
        'organization': org,
    }
    discount = discount[0]
    serializer = DiscountSerializer(discount, data=discount_data)
    try:
        serializer.is_valid(raise_exception=True)
        serializer.update(discount, discount_data)
        return Response({"message": "discount edited"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_discount(request, id):
    org = request.org

    discount = Discount.objects.filter(
        pk=id,
        organization = org
    )

    if not discount.exists():
        return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
    discount = discount[0]
    discount.delete()
    return Response({"message": "discount deleted successfully"}, status=status.HTTP_200_OK)