from django.shortcuts import get_object_or_404, render
from hsabackend.models.organization import Organization
from hsabackend.models.contractor import Contractor
from hsabackend.models.service import Service
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.views.decorators.clickjacking import xframe_options_exempt
import os
 
def get_url():
    if "ENV" not in os.environ:
        return "http://localhost:8000"
    if os.environ["ENV"] == "DEV":
        return "https://hsa.ssankey.com"
    if os.environ["ENV"] == "PROD":
        return "https://hsa-app.starlitex.com"
    else:
        raise RuntimeError("The enviornment for the backend was not set correctly")

@xframe_options_exempt
@api_view(["GET"])
def getHTMLForm(request, id):
    org = get_object_or_404(Organization, pk=id)
    services    = Service.objects.filter(organization=org)
    contractors = Contractor.objects.filter(organization=org)

    response = render(
        request,
        "requests/requests.html",
        {
            "url": f"{get_url()}/api/create/request/{id}",
            "org_id":      id,
            "services":    services,
            "contractors": contractors,
        }
    )

    # remove X-Frame-Options so it will embed in an <iframe>
    response.headers.pop("X-Frame-Options", None)
    return response

