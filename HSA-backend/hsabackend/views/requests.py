from rest_framework.decorators import api_view
from hsabackend.models.organization import Organization
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.request import Request
from hsabackend.models.job import Job
from django.db.models import Q
from hsabackend.models.customer import Customer
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from utils.response_helpers import get_table_data


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_org_request_data(request):
    return get_table_data(request, "request")
    
@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_request(request,id):
    org = request.org
    req = Request.objects.filter(pk=id, organization=org)
    if not req.exists():
        return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)
    req[0].delete()
    return Response({"message": "Request Deleted successfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def approve_request(request, id):
    org = request.org
    req = Request.objects.filter(pk=id, organization=org)
    if not req.exists():
        return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)
    the_req = req[0]
    the_req.delete()

    cust = Customer.objects.create(
        first_name = the_req.requestor_first_name,
        last_name = the_req.requestor_last_name,
        email = the_req.requestor_email,
        phone_no = the_req.requestor_phone_no,
        notes = "",
        organization = org
    )

    new_job = Job(
        requestor_city = the_req.requestor_city,
        requestor_state = the_req.requestor_state,
        requestor_zip = the_req.requestor_zip,
        requestor_address = the_req.requestor_address,
        description = "",
        customer = cust
    )
    new_job.save() # don't need to validate when based off a valid request
    return Response({"message": "Request approved successfully"}, status=status.HTTP_200_OK)