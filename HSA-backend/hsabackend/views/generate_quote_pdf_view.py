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
