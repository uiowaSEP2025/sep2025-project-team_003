from rest_framework.decorators import api_view
from hsabackend.models.organization import Organization
from hsabackend.models.quote import Quote
from hsabackend.models.invoice import Invoice
from hsabackend.models.customer import Customer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded

@api_view(["GET"])
@check_authenticated_and_onboarded()
def getQuotesForInvoiceByCustomer(request, id):
    org = request.org
    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset',0)
    if not pagesize or not offset:
        return Response({"message": "missing pagesize or offset"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pagesize = int(pagesize)
        offset = int(offset)
    except:
        return Response({"message": "pagesize and offset must be int"}, status=status.HTTP_400_BAD_REQUEST)
    

    customer_qs = Customer.objects.filter(pk=id, organization=org)
    if not customer_qs.exists():
        return Response({"message": "The customer does not exist"}, status=status.HTTP_404_NOT_FOUND)

    offset = offset * pagesize

    quotes = Quote.objects.select_related("jobID").select_related("jobID__customer").filter(
        jobID__organization=org,            # Ensure the quote's job is linked to the user's organization
        status = "accepted",                # invoice must be accepted to bill
        jobID__job_status= "completed",     # job must be done to bill 
        jobID__customer__pk=id,             # quote must for the customer on the invoice
        invoice = None                      # must not have an existing invoice tied to it
    )[offset : offset + pagesize] 
    
    data = []

    for quote in quotes:
        data.append(quote.jsonForInvoiceTable())
    
    count = Quote.objects.filter(
        jobID__organization=org,            # Ensure the quote's job is linked to the user's organization
        status = "accepted",                # invoice must be accepted to bill
        jobID__job_status= "completed",     # job must be done to bill 
        jobID__customer__pk=id,             # quote must for the customer on the invoice
        invoice = None                      # must not have an existing invoice tied to it
    ).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)

@api_view(["GET"])
@check_authenticated_and_onboarded()
def getQuotesForInvoiceByInvoice(request, id):
    org = request.org
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

    invoice_qs = Invoice.objects.filter(
        customer__organization=org.pk,
        pk = id
        )
    
    if not invoice_qs.exists():
        return Response({"message": "The invoice does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    customer = invoice_qs[0].customer

    quotes = Quote.objects.select_related("jobID").select_related("jobID__customer").filter(
        jobID__organization=org,            # Ensure the quote's job is linked to the user's organization
        status = "accepted",                # invoice must be accepted to bill
        jobID__job_status= "completed",     # job must be done to bill 
        jobID__customer=customer).filter(
        Q(invoice=None) | Q(invoice=id)  # invoice is either None or a specific number
        )[offset : offset + pagesize]

    
    data = []

    for quote in quotes:
        data.append(quote.jsonForInvoiceTable())
    
    count = Quote.objects.filter(
        jobID__organization=org,            # Ensure the quote's job is linked to the user's organization
        status = "accepted",                # invoice must be accepted to bill
        jobID__job_status= "completed",     # job must be done to bill 
        jobID__customer=customer).filter(
        Q(invoice=None) | Q(invoice=id)  # invoice is either None or a specific number
        ).count()

    res = {
        'data': data,
        'totalCount': count
    }    
    return Response(res, status=status.HTTP_200_OK)