import io
import os

from django.core.mail import EmailMultiAlternatives
from fpdf import FPDF
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.job import Job
from hsabackend.models.organization import Organization
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.pdf_helpers import generate_pdf_customer_org_header, generate_table_for_specific_job, \
    generate_pdf, generate_signature_page


@api_view(["GET"])
@check_authenticated_and_onboarded
def generate_quote_pdf(request, job_id):
    return generate_pdf(request, job_id, "quote")


@api_view(["POST"])
@check_authenticated_and_onboarded
def send_quote_pdf_to_customer_email(request, id):
    org = Organization.objects.get(owning_User=request.user.pk)
    try:
        job = Job.objects.select_related("customer") \
            .get(pk=id, customer__organization=org.pk)
    except Job.DoesNotExist:
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times', size=12)

    generate_pdf_customer_org_header(pdf, org, job, "quote")
    generate_table_for_specific_job(pdf, job.pk, 1, 1)
    generate_signature_page(pdf)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    subject = f"Quote for Job #{job.pk}"
    from_email = os.environ.get('EMAIL_HOST_USER')
    to_email = job.customer.email

    text_content = (
        f"Hello {job.customer.first_name},\n\n"
        "Please find attached the PDF quote for your requested job.\n\n"
        "If you have any questions, reply to this email.\n\n"
        "Best,\n"
        "HSA Team"
    )

    html_content = f"""
        <p>Hello {job.customer.first_name},</p>
        <p>Please find attached the PDF quote for your requested job.</p>
        <p>If you have any questions, just hit reply.</p>
        <p>Best,<br/>HSA Team</p>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")

    filename = f"quote_job_{job.pk}.pdf"
    msg.attach(filename, buffer.getvalue(), "application/pdf")

    msg.send()

    return Response(
        {"message": f"Quote PDF sent to {to_email}"},
        status=status.HTTP_200_OK
    )