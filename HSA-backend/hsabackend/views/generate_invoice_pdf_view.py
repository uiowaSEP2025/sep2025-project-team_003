from django.http import HttpResponse
from rest_framework.response import Response
from fpdf import FPDF
import io
from hsabackend.models.job import Job
from rest_framework.decorators import api_view
from hsabackend.models.organization import Organization
from rest_framework import status   
from hsabackend.models.invoice import Invoice
from hsabackend.utils.pdf_utils import get_job_detailed_table
from hsabackend.utils.string_formatters import format_title_case, format_phone_number_with_parens, format_maybe_null_date, format_currency, format_tax_percent, format_date_to_iso_string
from decimal import Decimal
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.generate_qr_code import generate_qr_code
import os
import tempfile

def generate_pdf_customer_org_header(pdf: FPDF, org: Organization, invoice: Invoice):
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Times", size=12)
    col_width = pdf.w / 2 - 10  

    pdf.cell(col_width, 10, f"INVOICE ID: {invoice.pk}", align="L")
    pdf.cell(col_width, 10, f"{format_title_case(org.org_name)}", align="R")

    pdf.ln(5) # 5 is the space between lines

    pdf.cell(col_width, 10, f"{invoice.customer.last_name}, {invoice.customer.first_name}", align="L")
    pdf.cell(col_width, 10, f"{org.org_email}", align="R")

    pdf.ln(5) 

    pdf.cell(col_width, 10, f"{invoice.customer.email}", align="L")
    pdf.cell(col_width, 10, f"{format_phone_number_with_parens(org.org_phone)}", align="R")
    
    pdf.ln(5) 

    pdf.cell(col_width, 10, f"CUSTOMER ID: {invoice.customer.pk}", align="L")

    pdf.ln(10) 

    pdf.cell(col_width, 10, f"ISSUANCE DATE: {format_maybe_null_date(invoice.issuance_date)}", align="L")
    pdf.ln(5)
    pdf.cell(col_width, 10, f"DUE DATE: {format_maybe_null_date(invoice.due_date)}", align="L")
    pdf.ln(15) 



def generate_global_jobs_table(pdf:FPDF, invoice: Invoice):
    """
    generates the table showing all jobs, and returns a list of job ids representing the order of 
    the jobs that are included in the table in order, as well as the total amount
    """
    # no validation checks on if the org owns the quotes, thats done on creation
    jobs = Job.objects.filter(invoice=invoice)
    greyscale = 215 # higher no --> lighter grey
    with pdf.table(line_height=4, padding=2, text_align=("LEFT", "LEFT", "LEFT", "LEFT", "LEFT"), borders_layout="SINGLE_TOP_LINE", cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
        header = table.row()
        header.cell("Job Number")
        header.cell("Date")
        header.cell("Job Description")
        header.cell("Address")
        header.cell("Amount")

        total = Decimal(0)
        for j in jobs:
            r = table.row()
            r.cell(str(j.pk))
            r.cell(format_date_to_iso_string(j.start_date))
            r.cell(j.truncated_job_desc)
            r.cell(j.full_display_address)
            r.cell(format_currency(j.total_cost))
            total += Decimal(str(j.total_cost))

        # display total
        r = table.row()
        r.cell("Total:")
        r.cell("")
        r.cell("")
        r.cell("")
        r.cell(format_currency(total))

        # display tax %
        r = table.row()
        r.cell("Tax Percent:")
        r.cell("")
        r.cell("")
        r.cell("")
        r.cell(str(f"{invoice.tax} %"))
        #display tax amount
        math_tax = invoice.tax * Decimal("0.01")
        tax_amount = math_tax * total
        r = table.row()
        r.cell("Tax Amount:")
        r.cell("")
        r.cell("")
        r.cell("")
        r.cell(format_currency(tax_amount))

        #display grand total
        total_with_tax = total + tax_amount
        r = table.row()
        r.cell("Total With Tax:")
        r.cell("")
        r.cell("")
        r.cell("")
        r.cell(format_currency(total_with_tax))

    return (list(jobs), total_with_tax)

def add_total_and_disclaimer(pdf: FPDF, total, org_name, invoice: Invoice):
    disclaimer_text = """
        *Disclaimer: The information on this invoice has been consolidated from reliable sources; however, 
        it may not always be entirely accurate. If you notice any discrepancies, please address them directly 
        with the handyman listed on the invoice. You remain responsible for paying the original agreed-upon 
        amount, regardless of any errors or inconsistencies in this document.
        """
    pdf.ln(5)
    pdf.set_left_margin(10) # don't remove or it will mess up alignment
    pdf.multi_cell(0, text=f"Please make payment to {format_title_case(org_name)} for amount {format_currency(total)}*", align="L")
    pdf.ln(5)

    # Add QR code if payment_link exists
    if invoice.payment_url:
        # Generate QR code
        qr_img = generate_qr_code(invoice.payment_url)

        # Create a temporary file for the QR code
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_img_path = temp_file.name
            qr_img.save(temp_img_path)

        try:
            # Position QR code at the bottom right
            qr_size = 30  # Size of QR code in mm
            pdf.image(temp_img_path, x=pdf.w - qr_size - 10, y=pdf.h - qr_size - 40, w=qr_size)

            # Add a label for the QR code
            pdf.set_xy(pdf.w - qr_size - 10, pdf.h - 35)
            pdf.set_font("Times", size=8)
            pdf.cell(qr_size, 5, "Scan to pay", align="C")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_img_path):
                os.unlink(temp_img_path)

    pdf.set_left_margin(0) # don't remove or it will mess up alignment
    pdf.set_y(-40)  # Move to 40 units above the bottom
    pdf.multi_cell(0, text=disclaimer_text, align="C")

def add_job_header(pdf, job):
    pdf.set_font("Arial", size=12, style='B')
    pdf.set_xy(10, 20)
    pdf.cell(10, 10, f"Job {job.pk} - {job.truncated_job_desc}", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.set_xy(10, 30)
    pdf.cell(10, 10, f"Start Date: {format_date_to_iso_string(job.start_date)}", ln=True)
    pdf.set_xy(10, 40)
    pdf.cell(10, 10, f"Address: {job.full_display_address}", ln=True)
    pdf.ln(5)  # Add some space between the header and the table



@api_view(["GET"])
@check_authenticated_and_onboarded()
def generate_pdf(request, id):
    org = request.org

    invoice_qs = Invoice.objects.select_related("customer").filter(
        customer__organization=org.pk,
        pk = id
        )
    
    if not invoice_qs.exists():
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times')

    inv = invoice_qs[0] 

    generate_pdf_customer_org_header(pdf,org,inv)
    jobs, total = generate_global_jobs_table(pdf, inv)
    pdf.add_page()
    for idx in range(len(jobs)):
        j = jobs[idx]
        add_job_header(pdf, j)
        get_job_detailed_table(pdf, j)
        if idx != len(jobs) - 1:
            pdf.add_page() # move to top of next page
    add_total_and_disclaimer(pdf, total, org.org_name, inv)

        

    # Save PDF to a BytesIO buffer
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)  # Reset buffer position

    # Create an HTTP response with the PDF as an attachment
    response = HttpResponse(pdf_buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="output.pdf"'  # or 'attachment;'
    
    return response