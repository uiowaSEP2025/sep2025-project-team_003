from django.shortcuts import get_object_or_404, render
from hsabackend.models.organization import Organization
from hsabackend.models.contractor import Contractor
from hsabackend.models.service import Service
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def getHTMLForm(request, id):
    org = get_object_or_404(Organization, pk=id)
    services    = Service.objects.filter(organization=org)
    contractors = Contractor.objects.filter(organization=org)

    resp = Response(
        {
            "org_id":       id,
            "services":     services,
            "contractors":  contractors,
        },
        template_name="requests/requests.html"
    )

    resp.headers.pop("X-Frame-Options", None)
    return resp
