from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.invoice import Invoice
from hsabackend.models.job import Job
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_table_data, get_individual_data, create_individual_data, \
    update_individual_data, delete_object


@api_view(["POST"])
@check_authenticated_and_onboarded()
def create_invoice(request):
    return create_individual_data(request, "invoice")

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_invoices(request):
    return get_table_data(request, "invoice")

@api_view(["POST"])
@check_authenticated_and_onboarded()
def update_invoice(request, invoice_id):
    return update_individual_data(request, invoice_id, "invoice")

@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_invoice(request, invoice_id):
    return delete_object(request, invoice_id, "invoice")
@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_invoice(request, invoice_id):
    return get_individual_data(request,  invoice_id, "invoice")

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_data_for_invoice(request, invoice_id):
    """gets all the data for the invoice detailed view"""
    org = request.organization
    invoice_qs = Invoice.objects.filter(
        customer__organization=org.pk,
        pk = invoice_id
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

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_quotes_for_invoice_by_customer(request, customer_id):
    return get_table_data(request, "customer_quotes", customer_id=customer_id)
