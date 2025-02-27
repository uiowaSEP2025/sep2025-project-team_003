from rest_framework.decorators import api_view
from hsabackend.models.organization import Organization
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.request import Request
from django.db.models import Q

@api_view(["GET"])
def get_org_request_data(request):
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
    
@api_view(["GET"])
def delete_request(request,id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    org = Organization.objects.get(owning_User=request.user.pk)
    req = Request.objects.filter(pk=id, organization=org)
    if not req.exists():
        return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)
    req[0].delete()
    return Response({"message": "Request Deleted successfully"}, status=status.HTTP_200_OK)