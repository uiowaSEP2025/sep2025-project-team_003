from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.request import Request
from hsabackend.serializers.customer_serializer import CustomerSerializer
from hsabackend.serializers.job_serializer import JobSerializer
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_table_data, delete_object


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_org_request_data(request):
    return get_table_data(request, "request")
    
@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_request(request,request_id):
    delete_object(request, request_id, "request")

@api_view(["POST"])
@check_authenticated_and_onboarded()
def approve_request(request, id):
    org = request.org
    req = Request.objects.filter(pk=id, organization=org)
    if not req.exists():
        return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)
    the_req = req[0]
    the_req.delete()

    customer_data = {
        "first_name": the_req.requestor_first_name,
        "last_name": the_req.requestor_last_name,
        "email": the_req.requestor_email,
        "phone": the_req.requestor_phone_no,
        "notes": "",
        "organization": org,
    }

    customer_serializer = CustomerSerializer(data=customer_data)
    if not customer_serializer.is_valid():
        return Response({"errors": customer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    customer_serializer.save()

    job_data = {
        "job_status": "created",
        "description": the_req.request_description,
        "organization": org,
        "customer": customer_serializer.instance,
        "job_address": the_req.requestor_address,
        "job_city": the_req.requestor_city,
        "job_state": the_req.requestor_state,
        "job_zip": the_req.requestor_zip,
    }
    job_serializer = JobSerializer(data=job_data, partial=True)
    if not job_serializer.is_valid():
        return Response({"errors": job_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    job_serializer.save()
    return Response({"message": "Request approved successfully"}, status=status.HTTP_200_OK)