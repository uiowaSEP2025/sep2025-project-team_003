from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.customer import Customer
from hsabackend.serializers.customer_serializer import CustomerSerializer
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_table_data


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_customer_table_data(request):
    return get_table_data(request, 'customer')

@api_view(["GET"])
@check_authenticated_and_onboarded(require_onboarding=False)
def get_customer_excluded_table_data(request):
    org = request.org
    search = request.query_params.get('search', '')
    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset',0)
    excluded_ids_str = request.GET.getlist('excludeIDs', [])
    excluded_ids = [int(id) for id in excluded_ids_str]

    if not pagesize or not offset:
        return Response({"message": "missing pagesize or offset"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pagesize = int(pagesize)
        offset = int(offset)
    except:
        return Response({"message": "pagesize and offset must be int"}, status=status.HTTP_400_BAD_REQUEST)
    
    offset = offset * pagesize
    customers = Customer.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).filter(
        Q(first_name__icontains=search) | Q(last_name__icontains=search) 
    )[offset:offset + pagesize] if search else Customer.objects.filter(organization=org.pk).exclude(id__in=excluded_ids)[offset:offset + pagesize]

    serializers = CustomerSerializer(customers, many=True)
    
    count = Customer.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).filter(
        Q(first_name__icontains=search) | Q(last_name__icontains=search)
    ).count() if search else Customer.objects.filter(organization=org.pk).exclude(id__in=excluded_ids).count()

    res = {
        'data': serializers.data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)
    
@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def create_customer(request):
    org = request.org
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    email = request.data.get('email', '')
    phone = request.data.get('phone', '').replace("-","")
    notes = request.data.get('notes', '')
    customer_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "notes": notes,
        "organization": org,
    }

    serializer = CustomerSerializer(data=customer_data)

    try:
        serializer.is_valid()  # Validate the model instance
        serializer.create(customer_data)
        return Response({"message": "Customer created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_customer(request, id):
    org = request.org
    customer_qs = Customer.objects.filter(pk=id, organization=org)
    if not customer_qs.exists():
        return Response({"message": "The customer does not exist"}, status=status.HTTP_404_NOT_FOUND)
    customer = customer_qs[0]
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    email = request.data.get('email', '')
    phone = request.data.get('phone', '')
    notes = request.data.get('notes', '')
    customer_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "notes": notes,
        "organization": org,
    }

    serializer = CustomerSerializer(data=customer_data)
    
    try:
        serializer.is_valid()  # Validate the model instance
        serializer.update(customer, customer_data)
        return Response({"message": "Customer edited successfully"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@check_authenticated_and_onboarded(require_onboarding=False)
def delete_customer(request, id):
    org = request.org
    cust = Customer.objects.filter(pk=id, organization=org)
    if not cust.exists():
        return Response({"message": "The customer does not exist"}, status=status.HTTP_404_NOT_FOUND)
    cust[0].delete()
    return Response({"message": "Customer Deleted successfully"}, status=status.HTTP_200_OK)
