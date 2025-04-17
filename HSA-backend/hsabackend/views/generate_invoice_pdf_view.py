from django.http import HttpResponse
from rest_framework.response import Response
from fpdf import FPDF
import io
from rest_framework.decorators import api_view
from hsabackend.models.organization import Organization
from rest_framework import status   
from hsabackend.models.invoice import Invoice
from hsabackend.utils.string_formatters import format_title_case, format_phone_number_with_parens, format_maybe_null_date, format_currency, format_percent, format_tax_percent
from decimal import Decimal

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
    quotes = Quote.objects.select_related("jobID").select_related("discount_type").filter(
        invoice=invoice
    ).order_by("-jobID__end_date")
    res = []
    greyscale = 215 # higher no --> lighter grey
    with pdf.table(line_height=4, padding=2, text_align=("LEFT", "LEFT", "LEFT", "LEFT", "LEFT"), borders_layout="SINGLE_TOP_LINE", cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
        header = table.row()
        header.cell("Job Number")
        header.cell("Date")
        header.cell("Job Description")
        header.cell("Address")
        header.cell("Amount")
        
        # amount is a decimal type
        total = Decimal(0)
        total_discnt_aggregate = Decimal(0)

        cnt = 1
        for quote in quotes:
            res.append(quote.jobID.pk)
            quote_row = table.row()
            json = quote.geerate_invoice_global_table_json()
            quote_row.cell(str(cnt))
            quote_row.cell(json["Date"])
            quote_row.cell(json["Job Description"])
            quote_row.cell(json["Address"])
            total += json["Total Undiscounted"]
            quote_row.cell(str(json["Total Undiscounted"]))
            total_discnt_aggregate += json["Discount Percent"]
            cnt += 1

        undiscounted_total_row = table.row()
        undiscounted_total_row.cell("Original Total: ")
        undiscounted_total_row.cell("")
        undiscounted_total_row.cell("")
        undiscounted_total_row.cell("")
        undiscounted_total_row.cell(str(format_currency(total)))
        total_discnt_aggregate = total_discnt_aggregate/len(quotes) # ex 30.01%
        # this solution sucks so much ass, and I am open to discussing how to fix it
        math_discount_percent = Decimal((1-(total_discnt_aggregate/100)))

        discounted_total = total * math_discount_percent

        is_discounted = discounted_total != total

        discounted_amout = total # will be the full total if not is_discounted

        if is_discounted:
            discount_percent_row = table.row()
            discount_percent_row.cell("Discount Percent: ")
            discount_percent_row.cell("")
            discount_percent_row.cell("")
            discount_percent_row.cell("")
            discount_percent_row.cell(str(format_percent(total_discnt_aggregate)))

            discounted_amout = total * math_discount_percent
            discounted_price_row = table.row()
            discounted_price_row.cell("Discounted Price: ")
            discounted_price_row.cell("")
            discounted_price_row.cell("")
            discounted_price_row.cell("")
            discounted_price_row.cell(str(format_currency(discounted_amout)))

        tax_percent_row = table.row()
        tax_percent_row.cell("Tax Amount: ")
        tax_percent_row.cell("")
        tax_percent_row.cell("")
        tax_percent_row.cell("")
        tax_percent_row.cell(format_tax_percent(str(invoice.tax)))

        total_with_tax = (1 + invoice.tax) * discounted_amout
        tax_amount_row = table.row()
        tax_amount_row.cell("Tax Amount: ")
        tax_amount_row.cell("")
        tax_amount_row.cell("")
        tax_amount_row.cell("")
        tax_amount_row.cell(str(format_currency(total_with_tax - discounted_amout)))

        grand_total_row = table.row()
        grand_total_row.cell("Total:")
        grand_total_row.cell("")
        grand_total_row.cell("")
        grand_total_row.cell("")
        grand_total_row.cell(str(format_currency(total_with_tax)))

    return (res, total_with_tax)

def add_total_and_disclaimer(pdf: FPDF, total, org_name):
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
    pdf.set_left_margin(0) # don't remove or it will mess up alignmentpdf.set_y(-20)  # Move to 20 units above the bottom
    pdf.set_y(-40)  # Move to 20 units above the bottom
    pdf.multi_cell(0, text=disclaimer_text, align="C")

def generate_table_for_specific_job(pdf: FPDF, jobid: int, num_jobs: int, idx: int):
    greyscale = 215 # higher no --> lighter grey
    pdf.set_x(10)
    pdf.multi_cell(100, text=f"Job #{idx + 1} of {num_jobs}", align="L")
    with pdf.table(line_height=4, padding=2, text_align=("LEFT", "LEFT", "LEFT", "LEFT", "LEFT"), borders_layout="SINGLE_TOP_LINE", cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
        header = table.row()
        header.cell("Services Rendered", colspan=2, align="C")
        services = JobService.objects.select_related("service").filter(
            job=jobid
        )
        for service in services:
            json = service.get_service_info_for_detailed_invoice()
            service_row = table.row()
            service_row.cell(json["service name"])
            service_row.cell(json["service description"])

    pdf.ln(5) 

    with pdf.table(line_height=4, padding=2, text_align=("LEFT", "LEFT", "LEFT", "LEFT", "LEFT"), borders_layout="SINGLE_TOP_LINE", cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
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
    job_ids, total = generate_global_jobs_table(pdf, inv)
    add_total_and_disclaimer(pdf, total, org.org_name)
    # cursor is on page 2
    for i in range(len(job_ids)):
        generate_table_for_specific_job(pdf,job_ids[i], len(job_ids), i)
        if i != len(job_ids) - 1:
            pdf.add_page() # move to top of next page

    # Save PDF to a BytesIO buffer
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)  # Reset buffer position

    # Create an HTTP response with the PDF as an attachment
    response = HttpResponse(pdf_buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="output.pdf"'  # or 'attachment;'
    
    return response