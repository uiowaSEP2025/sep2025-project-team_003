import io
from decimal import Decimal

from django.http import HttpResponse
from fpdf import FPDF
from rest_framework import status
from rest_framework.response import Response
from hsabackend.models.invoice import Invoice
from hsabackend.models.job import JobsServices, JobsMaterials, Job
from hsabackend.models.organization import Organization
from hsabackend.serializers.job_material_serializer import JobMaterialSerializer
from hsabackend.serializers.job_service_serializer import JobServiceSerializer
from hsabackend.utils.string_formatters import format_currency, format_title_case, format_phone_number_with_parens, \
    format_maybe_null_date, format_percent, format_tax_percent


def generate_global_jobs_table(pdf: FPDF, invoice: Invoice):
    """
    generates the table showing all jobs and returns a list of job ids representing the order of
    the jobs that are included in the table in order, as well as the total amount
    """
    # no validation checks on if the org owns the quotes, that's done on creation
    res = []
    greyscale = 215  # higher no --> lighter grey
    with pdf.table(line_height=4, padding=2, text_align=("LEFT", "LEFT", "LEFT", "LEFT", "LEFT"),
                   borders_layout="SINGLE_TOP_LINE", cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
        header = table.row()
        header.cell("Job Number")
        header.cell("Date")
        header.cell("Job Description")
        header.cell("Address")
        header.cell("Amount")

        # the amount is a decimal type
        total = Decimal(0)
        total_discount_aggregate = Decimal(0)

        undiscounted_total_row = table.row()
        undiscounted_total_row.cell("Original Total: ")
        undiscounted_total_row.cell("")
        undiscounted_total_row.cell("")
        undiscounted_total_row.cell("")
        undiscounted_total_row.cell(str(format_currency(total)))
        total_discount_aggregate = invoice.discount_aggregate_percentage  # ex 30.01%
        # this solution sucks so much ass, and I am open to discussing how to fix it
        math_discount_percent = Decimal((1 - (total_discount_aggregate / 100)))

        discounted_total = total * math_discount_percent

        is_discounted = discounted_total != total

        discounted_amount = total  # will be the full total if not is_discounted

        if is_discounted:
            discount_percent_row = table.row()
            discount_percent_row.cell("Discount Percent: ")
            discount_percent_row.cell("")
            discount_percent_row.cell("")
            discount_percent_row.cell("")
            discount_percent_row.cell(str(format_percent(total_discount_aggregate)))

            discounted_amount = total * math_discount_percent
            discounted_price_row = table.row()
            discounted_price_row.cell("Discounted Price: ")
            discounted_price_row.cell("")
            discounted_price_row.cell("")
            discounted_price_row.cell("")
            discounted_price_row.cell(str(format_currency(discounted_amount)))

        tax_percent_row = table.row()
        tax_percent_row.cell("Tax Amount: ")
        tax_percent_row.cell("")
        tax_percent_row.cell("")
        tax_percent_row.cell("")
        tax_percent_row.cell(format_tax_percent(str(invoice.sales_tax_percent)))

        total_with_tax = (1 + invoice.sales_tax_percent) * discounted_amount
        tax_amount_row = table.row()
        tax_amount_row.cell("Tax Amount: ")
        tax_amount_row.cell("")
        tax_amount_row.cell("")
        tax_amount_row.cell("")
        tax_amount_row.cell(str(format_currency(total_with_tax - discounted_amount)))

        grand_total_row = table.row()
        grand_total_row.cell("Total:")
        grand_total_row.cell("")
        grand_total_row.cell("")
        grand_total_row.cell("")
        grand_total_row.cell(str(format_currency(total_with_tax)))

    return res, total_with_tax


def add_total_and_disclaimer(pdf: FPDF, total, org_name):
    disclaimer_text = """
        *Disclaimer: The information on this invoice has been consolidated from reliable sources; however, 
        it may not always be entirely accurate. If you notice any discrepancies, please address them directly 
        with the handyman listed on the invoice. You remain responsible for paying the original agreed-upon 
        amount, regardless of any errors or inconsistencies in this document.
        """
    pdf.ln(5)
    pdf.set_left_margin(10)  # don't remove or it will mess up the alignment
    pdf.multi_cell(0, text=f"Please make payment to {format_title_case(org_name)} for amount {format_currency(total)}*",
                   align="L")
    pdf.ln(5)
    pdf.set_left_margin(
        0)  # don't remove, or it will mess up the alignment pdf. (set_y(-20))  # Move to 20 units above the bottom
    pdf.set_y(-40)  # Move to 20 units above the bottom
    pdf.multi_cell(0, text=disclaimer_text, align="C")


def generate_pdf_customer_org_header(pdf: FPDF, org: Organization, job: Job, type_enum):
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Times", size=12)
    col_width = pdf.w / 2 - 10

    if type_enum == "quote":
        pdf.cell(col_width, 10, f"QUOTE FOR JOB ID: {job.pk}", align="L")
    else:
        pdf.cell(col_width, 10, f"INVOICE ID: {job.invoice.pk}", align="L")
    pdf.cell(col_width, 10, f"{format_title_case(org.org_name)}", align="R")

    pdf.ln(5)  # 5 is the space between lines

    pdf.cell(col_width, 10, f"{job.customer.last_name}, {job.customer.first_name}", align="L")
    pdf.cell(col_width, 10, f"{org.org_email}", align="R")

    pdf.ln(5)

    pdf.cell(col_width, 10, f"{job.customer.email}", align="L")
    pdf.cell(col_width, 10, f"{format_phone_number_with_parens(org.org_phone)}", align="R")

    pdf.ln(5)

    pdf.cell(col_width, 10, f"CUSTOMER ID: {job.customer.pk}", align="L")

    pdf.ln(10)

    if type_enum == "quote":
        pdf.cell(col_width, 10, f"START DATE: {format_maybe_null_date(job.start_date)}", align="L")
        pdf.ln(5)
        pdf.cell(col_width, 10, f"END DATE: {format_maybe_null_date(job.end_date)}", align="L")
    else:
        pdf.cell(col_width, 10, f"ISSUANCE DATE: {format_maybe_null_date(job.invoice.date_issued)}", align="L")
        pdf.ln(5)
        pdf.cell(col_width, 10, f"DUE DATE: {format_maybe_null_date(job.invoice.date_due)}", align="L")
    pdf.ln(15)


def generate_table_for_specific_job(pdf: FPDF, jobid: int, num_jobs: int, idx: int):
    greyscale = 215  # higher no --> lighter grey
    pdf.set_x(10)
    pdf.multi_cell(100, text=f"Job #{idx + 1} of {num_jobs}", align="L")
    with pdf.table(line_height=4, padding=2, text_align=("LEFT", "LEFT", "LEFT", "LEFT", "LEFT"),
                   borders_layout="SINGLE_TOP_LINE", cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
        header = table.row()
        services = JobsServices.objects.select_related("service").filter(
            job=jobid
        )
        service_serializer = JobServiceSerializer(services, many=True)
        header.cell("Services Rendered", colspan=3, align="C")
        services_data = service_serializer.data
        for service in services_data:
            service_row = table.row()
            service_row.cell(service["service_name"])
            service_row.cell(service["service_description"])
            service_row.cell(service["fee"])
    pdf.ln(5)

    with pdf.table(line_height=4, padding=2, text_align=("LEFT", "LEFT", "LEFT", "LEFT", "LEFT"),
                   borders_layout="SINGLE_TOP_LINE", cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
        materials = JobsMaterials.objects.select_related("material").filter(job=jobid)

        header = table.row()
        header.cell("Material Name")
        header.cell("Per Unit")
        header.cell("Units Used")
        header.cell("Total")

        total = Decimal(0)
        for mat in materials:
            material_row = table.row()
            material_row.cell(mat.material.name)
            material_row.cell(format_currency(mat.unit_price))
            material_row.cell(str(mat.quantity))
            total += mat.total_cost
            material_row.cell(format_currency(mat.total_cost))

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

def generate_pdf(request, job_id, type_enum="invoice"):
    org = request.org

    if type_enum == "quote":
        object_select = Job.objects.select_related("customer").filter(
        customer__organization=org.pk,
        pk=job_id
    )
    else:
        object_select = Invoice.objects.select_related("customer").filter(
            customer__organization=org.pk,
            pk=job_id
        )
    if not object_select.exists():
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times')

    obj = object_select[0]

    generate_pdf_customer_org_header(pdf, org, obj, type_enum)
    if type_enum == "quote":
        generate_table_for_specific_job(pdf, obj, 1, 1)
        # Add a second page with the legal statement and signature slot
        generate_signature_page(pdf)
    else:
        job_ids, total = generate_global_jobs_table(pdf, obj)
        add_total_and_disclaimer(pdf, total, org.org_name)
        # the cursor is on page 2
        for i in range(len(job_ids)):
            generate_table_for_specific_job(pdf, job_ids[i], len(job_ids), i)
            if i != len(job_ids) - 1:
                pdf.add_page()  # move to top of next page

    # Save PDF to a BytesIO buffer
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)  # Reset buffer position

    # Create an HTTP response with the PDF as an attachment
    response = HttpResponse(pdf_buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="output.pdf"'  # or 'attachment;'

    return response
