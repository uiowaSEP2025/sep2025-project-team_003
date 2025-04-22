from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import Q, Sum
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.customer import Customer
from hsabackend.models.invoice import Invoice
from hsabackend.models.job import Job
from hsabackend.models.organization import Organization
from hsabackend.utils.api_validators import parseAndReturnDate, parse_and_return_decimal
from decimal import Decimal
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded


@api_view(["POST"])
@check_authenticated_and_onboarded()
def create_invoice(request):
    json = request.data  
    org = request.org

    customer_id = json.get("customerID", None)
    if not isinstance(customer_id, int):
        return Response({"message": "CustomerID must be int"}, status=status.HTTP_400_BAD_REQUEST)

    job_ids = json.get("jobIDs", [])
    if not isinstance(job_ids, list):
        return Response({"message": "Jobs must be list"}, status=status.HTTP_400_BAD_REQUEST)

    if len(job_ids) == 0:
        return Response({"message": "Must include at least 1 job"}, status=status.HTTP_400_BAD_REQUEST)

    invoice_status = json.get("status",None)
    issued = parseAndReturnDate(json.get("issuedDate",""))
    due = parseAndReturnDate(json.get("dueDate",""))
    tax_percent = json.get("tax",None)

    if not invoice_status or invoice_status not in ('created', 'issued', 'paid'):
        return Response({"message": "Must include a valid status 'created' | 'issued' | 'paid'"}, status=status.HTTP_400_BAD_REQUEST)  

    if invoice_status == 'created':
        issued = due = None

    if invoice_status != 'created' and (not issued or not due):
        return Response({"message": "Must include valid issuance and due dates"}, status=status.HTTP_400_BAD_REQUEST)  

    if invoice_status != 'created' and due < issued:
        return Response({"message": "Due date can not be before the issuance date"}, status=status.HTTP_400_BAD_REQUEST)  

    if not parse_and_return_decimal(tax_percent):
        return Response({"message": "Tax must be a valid percentage of the form 0.XX"}, status=status.HTTP_400_BAD_REQUEST)  

    cust_qs = Customer.objects.filter(pk=int(customer_id), organization=org)

    if not cust_qs.exists():
        # will be here if user does not own the customer ID
        return Response({"message": "Must provide customer for the invoice."}, status=status.HTTP_404_NOT_FOUND)

    invoice = Invoice(
        customer = cust_qs[0],
        date_issued = issued,
        date_due = due,
        sales_tax_percent = parse_and_return_decimal(tax_percent),
        status=invoice_status
    )

    try:
        invoice.full_clean()
        invoice.save()

        # Associate the selected jobs with this invoice
        if job_ids:
            Job.objects.filter(pk__in=job_ids, customer__organization=org).update(invoice=invoice)

        # Add discounts if provided
        discount_ids = json.get("discountIDs", [])
        if isinstance(discount_ids, list) and discount_ids:
            invoice.discounts.add(*discount_ids)

    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)


    return Response({"message": "Invoice created"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@check_authenticated_and_onboarded()
def getInvoices(request):
    org = request.org
    search = request.query_params.get('search', '')
    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset',0)
    if not pagesize or not offset:
        return Response({"message": "missing pagesize or offset"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pagesize = int(pagesize)
        offset = int(offset)
    except:
        return Response({"message": "pagesize and offset must be int"}, status=status.HTTP_400_BAD_REQUEST)

    offset = offset * pagesize
    invoices = Invoice.objects.select_related("customer").filter(
        customer__organization=org.pk).filter(
        Q(customer__first_name__icontains=search) |
        Q(customer__last_name__icontains=search)   
    )[offset : offset + pagesize] 
    data = []

    for invoice in invoices:
        data.append(invoice.json())

    count = Invoice.objects.select_related("customer").filter(
        customer__organization=org.pk).filter(
        Q(customer__first_name__icontains=search) |
        Q(customer__last_name__icontains=search)   
    ).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def updateInvoice(request, id):
    org = request.org
    json = request.data  

    job_ids = json.get("jobIDs",[])

    if not isinstance(job_ids, list):
        return Response({"message": "Jobs must be list"}, status=status.HTTP_400_BAD_REQUEST)

    if len(job_ids) == 0:
        return Response({"message": "Must include at least 1 job"}, status=status.HTTP_400_BAD_REQUEST)

    invoice_status = json.get("status",None)

    if not invoice_status or invoice_status not in ('created', 'issued', 'paid'):
        return Response({"message": "Must include a valid status 'created' | 'issued' | 'paid'"}, status=status.HTTP_400_BAD_REQUEST)  

    issued = parseAndReturnDate(json.get("issuedDate",""))
    due = parseAndReturnDate(json.get("dueDate",""))
    tax_percent = json.get("tax",None)

    if invoice_status == 'created':
        issued = due = None

    if invoice_status != 'created' and (not issued or not due):
        return Response({"message": "Must include valid issuance and due dates"}, status=status.HTTP_400_BAD_REQUEST)  

    if invoice_status != 'created' and due < issued:
        return Response({"message": "Due date can not be before the issuance date"}, status=status.HTTP_400_BAD_REQUEST)  

    invoice_qs = Invoice.objects.filter(
        customer__organization=org.pk,
        pk = id
        )

    if not invoice_qs.exists():
        return Response({"message": "The invoice does not exist"}, status=status.HTTP_404_NOT_FOUND)
    customer = invoice_qs[0].customer

    invoice = invoice_qs[0]
    invoice.status = invoice_status
    invoice.date_issued = issued
    invoice.date_due = due
    invoice.sales_tax_percent = parse_and_return_decimal(tax_percent)

    try:
        invoice.full_clean()
        invoice.save()

        # Update the jobs associated with this invoice
        # First, clear any existing job associations
        Job.objects.filter(invoice=invoice).update(invoice=None)

        # Then, associate the selected jobs with this invoice
        if job_ids:
            Job.objects.filter(pk__in=job_ids, customer__organization=org).update(invoice=invoice)

        # Update discounts if provided
        discount_ids = json.get("discountIDs", [])
        if isinstance(discount_ids, list) and discount_ids:
            invoice.discounts.clear()
            invoice.discounts.add(*discount_ids)

    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Invoice updated successfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def deleteInvoice(request,id):
    org = request.org
    invoice_qs = Invoice.objects.filter(
        customer__organization=org.pk,
        pk = id
        )
    if not invoice_qs.exists():
        return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)
    invoice_qs[0].delete()
    return Response({"message": "Invoice Deleted successfully"}, status=status.HTTP_200_OK)

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_data_for_invoice(request, id):
    """gets all the data for the invoice detailed view"""
    org = request.org
    invoice_qs = Invoice.objects.filter(
        customer__organization=org.pk,
        pk = id
        )
    if not invoice_qs.exists():
        return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)

    invoice = invoice_qs[0]
    res = invoice.json_for_view_invoice()

    # Get all jobs associated with this invoice
    jobs = Job.objects.filter(invoice=invoice.pk)
    res_jobs = []

    for job in jobs:
        res_jobs.append(job.json_simplify())

    # Get the discount percentage from the invoice
    discount_percentage = invoice.discount_aggregate_percentage

    res["jobs"] = {
        "jobs": res_jobs,
        "subtotal": str(invoice.subtotal),
        "taxPercent": str(invoice.sales_tax_percent),
        "totalDiscount": str(discount_percentage),
        "discountedSubtotal": str(invoice.discounted_subtotal),
        "subtotalAfterDiscount": str(invoice.subtotal_after_discount),
        "taxableAmount": str(invoice.taxable_amount),
        "grandtotal": str(invoice.total)
    }

    return Response(res, status=status.HTTP_200_OK)
