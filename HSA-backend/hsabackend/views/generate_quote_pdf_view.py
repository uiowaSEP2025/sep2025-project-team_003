import os
from django.core.mail import EmailMultiAlternatives

from django.http import HttpResponse
from rest_framework.response import Response
from fpdf import FPDF
import io
from rest_framework.decorators import api_view
from hsabackend.models.organization import Organization
from rest_framework import status   
from hsabackend.models.job_material import JobMaterial
from hsabackend.models.job import Job
from hsabackend.models.quote import Quote
from hsabackend.utils.string_formatters import (
    format_title_case, 
    format_phone_number_with_parens, 
    format_maybe_null_date, 
    format_currency, 
    format_percent, 
    format_tax_percent
)
from decimal import Decimal
from hsabackend.models.job_service import JobService
import random

from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded

def get_url():
    if "ENV" not in os.environ:
        return "http://localhost:8000"
    if os.environ["ENV"] == "DEV":
        return "https://hsa.ssankey.com"
    if os.environ["ENV"] == "PROD":
        return "https://hsa-app.starlitex.com"
    else:
        raise RuntimeError("The enviornment for the backend was not set correctly")

def gen_signable_link(jobid: int):
    job = Job.objects.get(id=jobid)
    job.quote_sign_pin = str(random.randint(10_000_000, 99_999_999))
    job.save()

    return job.quote_sign_pin


def generate_pdf_customer_org_header(pdf: FPDF, org: Organization, invoice: Job):
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Times", size=12)
    col_width = pdf.w / 2 - 10  

    pdf.cell(col_width, 10, f"QUOTE FOR JOB ID: {invoice.pk}", align="L")
    pdf.cell(col_width, 10, f"{format_title_case(org.org_name)}", align="R")

    pdf.ln(5)  # Space between lines

    pdf.cell(col_width, 10, f"{invoice.customer.last_name}, {invoice.customer.first_name}", align="L")
    pdf.cell(col_width, 10, f"{org.org_email}", align="R")

    pdf.ln(5) 

    pdf.cell(col_width, 10, f"{invoice.customer.email}", align="L")
    pdf.cell(col_width, 10, f"{format_phone_number_with_parens(org.org_phone)}", align="R")
    
    pdf.ln(5) 

    pdf.cell(col_width, 10, f"CUSTOMER ID: {invoice.customer.pk}", align="L")

    pdf.ln(10) 

    pdf.cell(col_width, 10, f"START DATE: {format_maybe_null_date(invoice.start_date)}", align="L")
    pdf.ln(5)
    pdf.cell(col_width, 10, f"END DATE: {format_maybe_null_date(invoice.end_date)}", align="L")
    pdf.ln(15) 

def generate_table_for_specific_job(pdf: FPDF, jobid: int, num_jobs: int, idx: int):
    greyscale = 215  # Higher number -> lighter grey
    pdf.set_x(10)
    with pdf.table(line_height=4, padding=2, text_align=("LEFT", "LEFT", "LEFT", "LEFT", "LEFT"),
                   borders_layout="SINGLE_TOP_LINE", cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
        header = table.row()
        header.cell("Services Rendered", colspan=2, align="C")
        services = JobService.objects.select_related("service").filter(job=jobid)
        for service in services:
            json = service.get_service_info_for_detailed_invoice()
            service_row = table.row()
            service_row.cell(json["service name"])
            service_row.cell(json["service description"])

    pdf.ln(5) 

    with pdf.table(line_height=4, padding=2, text_align=("LEFT", "LEFT", "LEFT", "LEFT", "LEFT"),
                   borders_layout="SINGLE_TOP_LINE", cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
        materials = JobMaterial.objects.filter(job=jobid)
        
        header = table.row()
        header.cell("Material Name")
        header.cell("Per Unit")
        header.cell("Units Used")
        header.cell("Total")

        total = Decimal(0)
        for mat in materials:
            material_row = table.row()
            json = mat.invoice_material_row()
            material_row.cell(json["material name"])
            material_row.cell(format_currency(json["per unit"]))
            material_row.cell(str(json["units used"]))
            total += json["total"]
            material_row.cell(format_currency(json["total"]))

        total_row = table.row()
        total_row.cell("Materials Total")
        total_row.cell("")
        total_row.cell("")
        total_row.cell(format_currency(total))

def generate_signature_page(pdf: FPDF):
    # Add a new page for signature and legal statement
    pdf.add_page()
    pdf.set_font("Times", size=12)
    legal_statement = (
         "By signing this PDF, you agree that the above information looks accurate to you and accept the price. "
         "You also acknowledge that it does not include extra fees such as unexpected labor costs, materials, taxes, etc."
    )
    pdf.multi_cell(0, 10, legal_statement)
    pdf.ln(20)
    pdf.cell(0, 10, "Signature:", ln=True)
    # Draw a signature line
    left_margin = pdf.l_margin
    right_margin = pdf.w - pdf.r_margin
    current_y = pdf.get_y() + 5
    pdf.line(left_margin, current_y, right_margin, current_y)

@api_view(["GET"])
def generate_quote_pdf(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user.pk)

    job_select = Job.objects.select_related("customer").filter(
        customer__organization=org.pk,
        pk=id
    )
    if not job_select.exists():
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times')

    job = job_select[0] 

    generate_pdf_customer_org_header(pdf, org, job)
    generate_table_for_specific_job(pdf, job, 1, 1)
    # Add a second page with the legal statement and signature slot
    generate_signature_page(pdf)

    # Save PDF to a BytesIO buffer
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)  # Reset buffer position

    # Create an HTTP response with the PDF as an attachment
    response = HttpResponse(pdf_buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="output.pdf"'
    
    return response

@api_view(["GET"])
def generate_quote_pdf_as_base64(request, id):
    import os
import io
import base64
import random
from decimal import Decimal
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from fpdf import FPDF

from hsabackend.models.organization import Organization
from hsabackend.models.job import Job
from hsabackend.models.job_service import JobService
from hsabackend.models.job_material import JobMaterial
from hsabackend.models.quote import Quote  # if needed elsewhere
from hsabackend.utils.string_formatters import (
    format_title_case,
    format_phone_number_with_parens,
    format_maybe_null_date,
    format_currency,
)

def get_url():
    if "ENV" not in os.environ:
        return "http://localhost:8000"
    if os.environ["ENV"] == "DEV":
        return "https://hsa.ssankey.com"
    if os.environ["ENV"] == "PROD":
        return "https://hsa-app.starlitex.com"
    raise RuntimeError("The environment for the backend was not set correctly")

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
    grey = 215
    pdf.set_x(10)
    with pdf.table(line_height=5, padding=2,
                   text_align=("LEFT",)*5,
                   borders_layout="SINGLE_TOP_LINE",
                   cell_fill_color=grey,
                   cell_fill_mode="ROWS") as tbl:
        hdr = tbl.row()
        hdr.cell("Services Rendered", colspan=2, align="C")
        for svc in JobService.objects.select_related("service").filter(job=job):
            info = svc.get_service_info_for_detailed_invoice()
            row = tbl.row()
            row.cell(info["service name"])
            row.cell(info["service description"])
    pdf.ln(5)

    # Materials table
    with pdf.table(line_height=5, padding=2,
                   text_align=("LEFT",)*4,
                   borders_layout="SINGLE_TOP_LINE",
                   cell_fill_color=grey,
                   cell_fill_mode="ROWS") as tbl:
        hdr = tbl.row()
        hdr.cell("Material Name")
        hdr.cell("Per Unit")
        hdr.cell("Units Used")
        hdr.cell("Total")

        total = Decimal(0)
        for mat in JobMaterial.objects.filter(job=job):
            info = mat.invoice_material_row()
            r = tbl.row()
            r.cell(info["material name"])
            r.cell(format_currency(info["per unit"]))
            r.cell(str(info["units used"]))
            total += info["total"]
            r.cell(format_currency(info["total"]))

        tr = tbl.row()
        tr.cell("Materials Total")
        tr.cell("", colspan=2)
        tr.cell(format_currency(total))

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
        return Response({"message": "Invalid credentials"},
                        status=status.HTTP_401_UNAUTHORIZED)

    org = Organization.objects.get(owning_User=request.user.pk)
    try:
        job = Job.objects.select_related("customer") \
                     .get(pk=id, customer__organization=org.pk)
    except Job.DoesNotExist:
        return Response({"message": "Not found"},
                        status=status.HTTP_404_NOT_FOUND)

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
        return Response({"message": "Not found"},
                        status=status.HTTP_404_NOT_FOUND)

    provided_pin = str(request.data.get("pin", ""))
    if provided_pin != job.quote_sign_pin:
        return Response({"message": "Invalid PIN"},
                        status=status.HTTP_403_FORBIDDEN)

    # If a link is already set, refuse to regenerate
    if job.quote_s3_link:
        return Response(
            {"message": "Quote has already been generated",
             "link": job.quote_s3_link},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Build PDF and return as base64
    org = job.customer.organization  # or however you get the org
    pdf_bytes = _build_quote_pdf(job, org)
    pdf_b64 = base64.b64encode(pdf_bytes).decode("ascii")

    return Response(
        {"quote_pdf_base64": pdf_b64},
        status=status.HTTP_200_OK
    )

@api_view(["POST"])
def send_quote_pdf_to_customer_email(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    org = Organization.objects.get(owning_User=request.user.pk)
    try:
        job = Job.objects.select_related("customer") \
            .get(pk=id, customer__organization=org.pk)
    except Job.DoesNotExist:
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times', size=12)

    generate_pdf_customer_org_header(pdf, org, job)
    generate_table_for_specific_job(pdf, job.pk, 1, 1)
    generate_signature_page(pdf)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    subject = f"Quote for Job #{job.pk}"
    from_email = os.environ.get('EMAIL_HOST_USER')
    to_email = job.customer.email

    pin = gen_signable_link(id)

    text_content = (
        f"Hello {job.customer.first_name},\n\n"
        f"Please find attached the PDF quote for your requested job, and make a statement at {get_url()}/signquote. Use pincode {pin} to access signable window.\n\n"
    )

    html_content = f"""
        <p>Hello {job.customer.first_name},</p>
        <p>{text_content}</p>
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