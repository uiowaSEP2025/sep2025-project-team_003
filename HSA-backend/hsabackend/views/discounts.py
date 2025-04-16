from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.discount_type import DiscountType
from django.db.models import Q
from django.core.exceptions import ValidationError
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_discounts(request):
    org = request.org
    search = request.query_params.get('search', '')
    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset',0)
    if not pagesize or not offset:
        return Response({"message": "missing pagesize or offset"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pagesize = int(pagesize)
        offset = int(offset)
    except:
        return Response({"message": "pagesize and offset must be int"}, status=status.HTTP_400_BAD_REQUEST)
    offset = offset * pagesize
    discounts = DiscountType.objects.filter(
        organization=org.pk).filter(
        Q(discount_name__icontains=search) 
    )[offset : offset + pagesize] 
    data = []

    for d in discounts:
        data.append(d.json_for_discount_table())
    
    count = DiscountType.objects.filter(
        organization=org.pk).filter(
        Q(discount_name__icontains=search) 
    ).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def create_discount(request):
    org = request.org
    name = request.data.get('name', '')
    percent = request.data.get('percent', '')

    
    discount = DiscountType(
        discount_name = name,
        discount_percent = percent,
        organization = org
    )
    try:
        discount.full_clean()
        discount.save()
        return Response({"messsage": "discount created"}, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_discount(request,id):
    org = request.org
    name = request.data.get('name', '')
    percent = request.data.get('percent', '')

    discount = DiscountType.objects.filter(
        pk=id,
        organization = org
    )

    if not discount.exists():
        return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
    discount = discount[0]
    discount.discount_name = name
    discount.discount_percent = percent
    try:
        discount.full_clean()
        discount.save()
        return Response({"message": "discount edited"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_discount(request, id):
    org = request.org

    discount = DiscountType.objects.filter(
        pk=id,
        organization = org
    )

    if not discount.exists():
        return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
    discount = discount[0]
    discount.delete()
    return Response({"message": "discount deleted successfully"}, status=status.HTTP_200_OK)