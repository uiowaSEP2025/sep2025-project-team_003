from rest_framework.decorators import api_view
from hsabackend.models.organization import Organization
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.request import Request
from hsabackend.models.job import Job
from django.db.models import Q
from hsabackend.models.customer import Customer
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded

@api_view(["POST"])
def create_request(request, id):
    """
    Public: create a new Request for org=id.
    Rate-limit this endpoint via DRF throttling or similar!
    """
    try:
        org = Organization.objects.get(pk=id)
    except Organization.DoesNotExist:
        return Response(
            {"message": f"Organization {id} not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    data = request.data

    # 2) build the Request instance (job left as None)
    req = ServiceRequest(
        requester_first_name = data.get("requester_first_name", "").strip(),
        requester_last_name  = data.get("requester_last_name",  "").strip(),
        requester_email      = data.get("requester_email",      "").strip(),
        requester_city       = data.get("requester_city",       "").strip(),
        requester_state      = data.get("requester_state",      "").strip(),
        requester_zip        = data.get("requester_zip",        "").strip(),
        requester_address    = data.get("requester_address",    "").strip(),
        requester_phone      = data.get("requester_phone",      "").replace("-", "").strip(),
        description          = data.get("description",          "").strip(),
        availability         = data.get("availability",         "").strip(),
        organization         = org,
        job                  = None,
    )

    # 3) validate & save
    try:
        req.full_clean()
        req.save()
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    # 4) return the new id + full JSON
    return Response(
        {
            "message": "Request created successfully",
            "id":      req.id,
            "data":    req.json(),
        },
        status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_org_request_data(request):
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
    
    requests = Request.objects.filter(organization=org.pk).filter(
        Q(name__icontains=search))[offset:offset + pagesize] if search else Request.objects.filter(
        organization=org.pk)[offset:offset + pagesize]

    data = []
    for req in requests:
        data.append(req.json())
    
    count = requests = Request.objects.filter(organization=org.pk).filter(
        Q(name__icontains=search)).count() if search else Request.objects.filter(
        organization=org.pk).count()
    
    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

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