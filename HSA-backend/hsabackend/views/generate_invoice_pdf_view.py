from rest_framework.decorators import api_view

from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.pdf_helpers import generate_pdf


@api_view(["GET"])
@check_authenticated_and_onboarded()
def generate_invoice_pdf(request, job_id):
    return generate_pdf(request, job_id, "invoice")