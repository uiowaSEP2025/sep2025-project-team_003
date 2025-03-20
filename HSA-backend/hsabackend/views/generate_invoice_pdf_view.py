from django.http import HttpResponse
from rest_framework.response import Response
from fpdf import FPDF
import io
from rest_framework.decorators import api_view
from hsabackend.models.organization import Organization
from rest_framework import status   
from hsabackend.models.invoice import Invoice
from hsabackend.models.organization import Organization
from hsabackend.models.quote import Quote
from hsabackend.utils.string_formatters import format_title_case, format_phone_number_with_parens, format_maybe_null_date, format_currency

def generate_pdf_customer_org_header(pdf: FPDF, org: Organization, invoice: Invoice):
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Times", size=12)
    col_width = pdf.w / 2 - 10  

    pdf.cell(col_width, 10, f"INVOICE ID: #{invoice.pk}", align="L")
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
    quotes = Quote.objects.select_related("jobID").select_related("discount_type").filter(
        invoice=invoice
    ).order_by("-jobID__end_date")
    res = []
    with pdf.table(line_height=4, padding=2, text_align=("LEFT", "LEFT", "LEFT", "LEFT", "LEFT")) as table:
        # headers
        cell_border = "TOP"

        row = table.row()
        row.cell("Job Number", border=cell_border)
        row.cell("Date",border=cell_border)
        row.cell("Job Description", border=cell_border)
        row.cell("Address", border=cell_border)
        row.cell("Amount", border=cell_border)
        
        # amount is a decimal type
        total = 0

        cnt = 1
        for quote in quotes:
            res.append(quote.jobID.pk)
            row = table.row()
            json = quote.geerate_invoice_global_table_json()
            row.cell(str(cnt), border=cell_border)
            row.cell(json["Date"], border=cell_border)
            row.cell(json["Job Description"], border=cell_border)
            row.cell(json["Address"], border=cell_border)
            total += json["Amount"]
            row.cell(str(format_currency(json["Amount"])), border=cell_border)
            cnt += 1

        totals_row = table.row()
        totals_row.cell("Total:", border=cell_border)
        totals_row.cell("", border=cell_border)
        totals_row.cell("", border=cell_border)
        totals_row.cell("", border=cell_border)
        totals_row.cell(str(format_currency(total)), border=cell_border)






@api_view(["GET"])
def generate_pdf(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user.pk)

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
    generate_global_jobs_table(pdf, inv)

    # Save PDF to a BytesIO buffer
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)  # Reset buffer position

    # Create an HTTP response with the PDF as an attachment
    response = HttpResponse(pdf_buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="output.pdf"'  # or 'attachment;'
    
    return response