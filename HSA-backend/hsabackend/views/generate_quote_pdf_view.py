import os
import io
import base64
import random
from datetime import datetime
from hsabackend.utils.env_utils import get_url
import boto3
from fpdf import FPDF
from hsabackend.utils.pdf_utils import get_job_detailed_table
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from hsabackend.models.organization import Organization
from hsabackend.models.job import Job
from hsabackend.models.job_service import JobService
from hsabackend.models.job_material import JobMaterial
from hsabackend.utils.string_formatters import (
    format_title_case,
    format_phone_number_with_parens,
    format_maybe_null_date,
    
)
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded


def gen_signable_link(job: Job) -> str:
    pin = str(random.randint(10_000_000, 99_999_999))
    job.quote_sign_pin = pin
    job.save(update_fields=["quote_sign_pin"])
    return pin


def _build_quote_pdf(job: Job, org: Organization) -> bytes:
    """Create the PDF in memory and return its bytes."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=12)

    # Header
    pdf.set_auto_page_break(auto=True, margin=15)
    col = pdf.w / 2 - 10
    pdf.cell(col, 10, f"QUOTE FOR JOB ID: {job.pk}", align="L")
    pdf.cell(col, 10, format_title_case(org.org_name), align="R")
    pdf.ln(5)
    pdf.cell(col, 10, f"{job.customer.last_name}, {job.customer.first_name}", align="L")
    pdf.cell(col, 10, org.org_email, align="R")
    pdf.ln(5)
    pdf.cell(col, 10, job.customer.email, align="L")
    pdf.cell(col, 10, format_phone_number_with_parens(org.org_phone), align="R")
    pdf.ln(5)
    pdf.cell(col, 10, f"CUSTOMER ID: {job.customer.pk}", align="L")
    pdf.ln(10)
    pdf.cell(col, 10, f"START DATE: {format_maybe_null_date(job.start_date)}", align="L")
    pdf.ln(5)
    pdf.cell(col, 10, f"END DATE: {format_maybe_null_date(job.end_date)}", align="L")
    pdf.ln(15)

    # Services table
    get_job_detailed_table(pdf, job)

    # Signature page
    pdf.add_page()
    pdf.set_font("Times", size=12)
    legal = (
        "By signing this PDF, you agree that the above information looks accurate to you "
        "and accept the price. You also acknowledge that it does not include extra fees "
        "such as unexpected labor costs, materials, taxes, etc."
    )
    pdf.multi_cell(0, 10, legal)
    pdf.ln(20)
    pdf.cell(0, 10, "Signature:", ln=True)
    y = pdf.get_y() + 5
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)

    buf = io.BytesIO()
    pdf.output(buf)
    return buf.getvalue()


@api_view(["GET"])
def generate_quote_pdf(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    org = Organization.objects.get(owning_User=request.user.pk)
    try:
        job = Job.objects.select_related("customer").get(pk=id, customer__organization=org.pk)
    except Job.DoesNotExist:
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    pdf_bytes = _build_quote_pdf(job, org)
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="quote_{job.pk}.pdf"'
    return response


@api_view(["POST"])
def generate_quote_pdf_as_base64(request, id):
    """
    Expects JSON body: { "pin": "12345678" }
    Returns the PDF as a base64 string if the pin matches and no link exists yet.
    """
    try:
        job = Job.objects.get(pk=id)
    except Job.DoesNotExist:
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    provided_pin = str(request.data.get("pin", ""))
    if provided_pin != job.quote_sign_pin:
        return Response({"message": "Invalid PIN"}, status=status.HTTP_403_FORBIDDEN)

    if job.quote_s3_link:
        return Response(
            {"message": "Quote has already been generated", "link": job.quote_s3_link},
            status=status.HTTP_400_BAD_REQUEST,
        )

    org = job.customer.organization
    pdf_bytes = _build_quote_pdf(job, org)
    pdf_b64 = base64.b64encode(pdf_bytes).decode("ascii")

    return Response({"quote_pdf_base64": pdf_b64}, status=status.HTTP_200_OK)


@api_view(["POST"])
def sign_the_quote(request, id):
    """
    Expects JSON body: { "quote_pdf_base64": "<base64-string>" }
    Decodes and uploads the signed PDF to S3 (public), marks the job pending, and returns the link.
    """
    try:
        job = Job.objects.get(pk=id)
    except Job.DoesNotExist:
        return Response({"message": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

    b64 = request.data.get("signed_pdf_base64")
    if not b64:
        return Response({"message": "Missing PDF data"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pdf_bytes = base64.b64decode(b64)
    except (TypeError, ValueError):
        return Response({"message": "Invalid base64 data"}, status=status.HTTP_400_BAD_REQUEST)

    bucket = os.environ.get("AWS_BUCKET")
    if not bucket:
        return Response({"message": "AWS_BUCKET not configured"}, status=status.HTTP_400_BAD_REQUEST)
    if "AWS_ENDPOINT" in os.environ:
        s3 = boto3.client(
            service_name ="s3",
            endpoint_url = os.environ["AWS_ENDPOINT"],
            region_name="auto", # Must be one of: wnam, enam, weur, eeur, apac, auto
        )
    else:
        s3 = boto3.client("s3")

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    key = f"quotes/quote_{job.pk}_signed_{timestamp}.pdf"

    try:
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=pdf_bytes,
            ContentType="application/pdf",
            ACL="public-read"
        )
    except Exception as e:
        return Response({"message": f"S3 upload failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    job.quote_s3_link = key
    job.quote_status = "created"
    job.save(update_fields=["quote_s3_link", "quote_status"])

    return Response({"status": job.quote_status, "quote_s3_link": job.quote_s3_link}, status=status.HTTP_200_OK)


@api_view(["POST"])
def send_quote_pdf_to_customer_email(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    org = Organization.objects.get(owning_User=request.user.pk)
    try:
        job = Job.objects.select_related("customer").get(pk=id, customer__organization=org.pk)
    except Job.DoesNotExist:
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    # Build PDF
    pdf_bytes = _build_quote_pdf(job, org)

    # Prepare email
    subject = f"Quote for Job #{job.pk}"
    from_email = os.environ.get("EMAIL_HOST_USER")
    to_email = job.customer.email
    pin = gen_signable_link(job)

    text_content = (
        f"Hello {job.customer.first_name},\n\n"
        f"Please find attached the PDF quote for your requested job, and make a statement at {get_url()}/signquote. "
        f"Use pincode {pin} to access signable window.\n\n"
    )
    html_content = f"""
        <p>Hello {job.customer.first_name},</p>
        <p>{text_content}</p>
        <p>If you have any questions, just hit reply.</p>
        <p>Best,<br/>HSA Team</p>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.attach(f"quote_job_{job.pk}.pdf", pdf_bytes, "application/pdf")
    msg.send()
    return Response({"message": f"Quote PDF sent to {to_email}"}, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_list_of_quotes_by_org(request):

    try:
        org = Organization.objects.get(owning_User=request.user.pk)
    except Organization.DoesNotExist:
        return Response({"message": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

    filterby = request.query_params.get("filterby", None)

    jobs = Job.objects.select_related("customer").filter(customer__organization=org)

    if filterby:
        filterby = filterby.lower()
        if filterby not in {"created", "accepted", "rejected"}:
            return Response({"message": "Invalid filter"}, status=status.HTTP_400_BAD_REQUEST)
        jobs = jobs.filter(quote_status=filterby)

    result = []
    for job in jobs:
        result.append({
            "job_id": job.pk,
            "customer_name": f"{job.customer.first_name} {job.customer.last_name}",
            "quote_status": job.quote_status,
            "quote_s3_link": job.quote_s3_link,
            "start_date": format_maybe_null_date(job.start_date),
            "end_date": format_maybe_null_date(job.end_date),
        })

    return Response({"data":result}, status=status.HTTP_200_OK)

@api_view(["GET"])
def retrieve_quote(request, id):

    try:
        org = Organization.objects.get(owning_User=request.user.pk)
    except Organization.DoesNotExist:
        return Response({"message": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        job = Job.objects.select_related("customer__organization") \
            .get(pk=id, customer__organization=org)
    except Job.DoesNotExist:
        return Response({"message": "Job not found or access denied"}, status=status.HTTP_404_NOT_FOUND)

    key = job.quote_s3_link
    if not key:
        return Response({"message": "No signed quote available"}, status=status.HTTP_404_NOT_FOUND)

    bucket = os.environ.get("AWS_BUCKET")
    if not bucket:
        return Response({"message": "AWS_BUCKET not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if "AWS_ENDPOINT" in os.environ:
        s3 = boto3.client(
            service_name="s3",
            endpoint_url=os.environ["AWS_ENDPOINT"],
            region_name="auto",  # as before
        )
    else:
        s3 = boto3.client("s3")

    try:
        presigned_url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=3600  # 1 hour
        )
    except Exception as e:
        return Response(
            {"message": "Could not generate presigned URL", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({"url": presigned_url}, status=status.HTTP_200_OK)

@api_view(["POST"])
def accept_reject_quote(request, id):
    """
    POST /api/quotes/<id>/accept_reject/
    Body: { "decision": "accept" | "reject" }
    """
    try:
        org = Organization.objects.get(owning_User=request.user.pk)
    except Organization.DoesNotExist:
        return Response({"message": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        job = Job.objects.select_related("customer__organization")\
            .get(pk=id, customer__organization=org)
    except Job.DoesNotExist:
        return Response({"message": "Job not found or access denied"}, status=status.HTTP_404_NOT_FOUND)

    if job.quote_status != "created":
        return Response(
            {"message": f"Cannot {request.data.get('decision')} when quote_status is '{job.quote_status}'"},
            status=status.HTTP_400_BAD_REQUEST
        )

    decision = str(request.data.get("decision", "")).lower()
    if decision not in ("accept", "reject"):
        return Response(
            {"message": "Invalid decision; must be 'accept' or 'reject'"},
            status=status.HTTP_400_BAD_REQUEST
        )

    customer_email = job.customer.email
    from_email = os.environ.get("EMAIL_HOST_USER") or settings.DEFAULT_FROM_EMAIL

    if decision == "accept":
        job.quote_status = "accepted"
        subject = f"Quote #{job.pk} Approved"
        text = (
            f"Hello {job.customer.first_name},\n\n"
            f"Thank you! Your quote for Job #{job.pk} has been accepted.\n\n"
            "We’ll be in touch shortly to schedule the work.\n\n"
            "Best,\nHSA Team"
        )
    else:  
        job.quote_status = "rejected"
        job.quote_s3_link = None
        subject = f"Quote #{job.pk} Rejected"
        sign_url = f"{get_url()}/signquote?job_id={job.pk}"
        text = (
            f"Hello {job.customer.first_name},\n\n"
            f"Your quote for Job #{job.pk} was rejected.\n\n"
            f"If you’d like to make changes and sign again, please visit:\n{sign_url}\n\n"
            "Feel free to reach out with any questions.\n\n"
            "Best,\nHSA Team"
        )

    job.save(update_fields=["quote_status", "quote_s3_link"] if decision == "reject" else ["quote_status"])

    msg = EmailMultiAlternatives(subject, text, from_email, [customer_email])
    msg.send()

    return Response(
        {"quote_status": job.quote_status},
        status=status.HTTP_200_OK
    )
