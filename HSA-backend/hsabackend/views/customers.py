from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization
from hsabackend.models.customer import Customer
from django.db.models import Q
from django.core.exceptions import ValidationError

@api_view(["GET"])
def get_customer_table_data(request):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    org = Organization.objects.get(owning_User=request.user.pk)
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
    
    customers = Customer.objects.filter(organization=org.pk).filter(
        Q(first_name__icontains=search) | Q(last_name__icontains=search) 
    )[offset:offset + pagesize] if search else Customer.objects.filter(organization=org.pk)[offset:offset + pagesize]

    data = []
    for cust in customers:
        data.append(cust.json())
    
    count = Customer.objects.filter(organization=org.pk).filter(
        Q(first_name__icontains=search) | Q(last_name__icontains=search)
    ).count() if search else Customer.objects.filter(organization=org.pk).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)
    
@api_view(["POST"])
def create_customer(request):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    org = Organization.objects.get(owning_User=request.user)
    first_name = request.data.get('firstn', '')
    last_name = request.data.get('lastn', '')
    email = request.data.get('email', '')
    phone_no = request.data.get('phoneno', '')
    notes = request.data.get('notes', '')
    customer = Customer(
        first_name = first_name,
        last_name = last_name,
        email = email,
        phone_no = phone_no,
        notes = notes,
        organization = org
    )
    try:
        customer.full_clean()  # Validate the model instance
        customer.save()
        return Response({"message": "Customer created successfully"}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def edit_customer(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    org = Organization.objects.get(owning_User=request.user)
    customer = Customer.objects.filter(pk=id, organization=org)
    if not customer.exists():
        return Response({"message": "The customer does not exist"}, status=status.HTTP_404_NOT_FOUND)
    first_name = request.data.get('firstn', '')
    last_name = request.data.get('lastn', '')
    email = request.data.get('email', '')
    phone_no = request.data.get('phoneno', '')
    notes = request.data.get('notes', '')
    
    customer.first_name = first_name
    customer.last_name = last_name
    customer.email = email
    customer.phone_no = phone_no
    customer.notes = notes
    
    try:
        customer.full_clean()  # Validate the model instance
        customer.save()
        return Response({"message": "Customer edited successfully"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def delete_customer(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    org = Organization.objects.get(owning_User=request.user.pk)
    cust = Customer.objects.filter(pk=id, organization=org)
    if not cust.exists():
        return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)
    cust[0].delete()
    return Response({"message": "Customer Deleted successfully"}, status=status.HTTP_200_OK)
