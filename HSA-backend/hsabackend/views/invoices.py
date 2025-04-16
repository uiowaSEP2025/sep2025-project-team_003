from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.customer import Customer 
from hsabackend.models.quote import Quote
from hsabackend.models.invoice import Invoice
from hsabackend.models.organization import Organization
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models import Sum
from hsabackend.utils.api_validators import parseAndReturnDate, parse_and_return_decimal
from decimal import Decimal
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded

@api_view(["POST"])
@check_authenticated_and_onboarded()
def createInvoice(request):
    json = request.data  
    org = request.org

    customer_id = json.get("customerID", None)
    quote_ids = json.get("quoteIDs",[])
    if not isinstance(customer_id, int):
        return Response({"message": "CustomerID must be int"}, status=status.HTTP_400_BAD_REQUEST)  
    
    if not isinstance(quote_ids, list):
        return Response({"message": "Quotes must be list"}, status=status.HTTP_400_BAD_REQUEST)  
    
    if len(quote_ids) == 0:
        return Response({"message": "Must include at least 1 quote"}, status=status.HTTP_400_BAD_REQUEST)  

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
        issuance_date = issued,
        due_date = due,
        tax = parse_and_return_decimal(tax_percent),
        status=invoice_status
    )
    
    try:
        invoice.full_clean()
        invoice.save()
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    
    Quote.objects.filter(
        pk__in=quote_ids, 
        jobID__organization=org,  # Ensure the quote's job is linked to the user's organization
        invoice = None, # Ensure this quote does not belong to other invoice
        status = "accepted",                # invoice must be accepted to bill
        jobID__job_status= "completed",      # job must be done to bill 
        jobID__customer= cust_qs[0]
    ).update(invoice=invoice)

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

    quote_ids = json.get("quoteIDs",[])

    if not isinstance(quote_ids, list):
        return Response({"message": "Quotes must be list"}, status=status.HTTP_400_BAD_REQUEST)  
    
    if len(quote_ids) == 0:
        return Response({"message": "Must include at least 1 quote"}, status=status.HTTP_400_BAD_REQUEST)  

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
    invoice.issuance_date = issued
    invoice.due_date = due
    invoice.tax = parse_and_return_decimal(tax_percent)

    try:
        invoice.full_clean()
        invoice.save()
    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    Quote.objects.filter(
        pk__in=quote_ids, 
        jobID__organization=org,            # Ensure the quote's job is linked to the user's organization
        status = "accepted",                # quote must be accepted to bill
        jobID__job_status= "completed",     # job must be done to bill 
        jobID__customer=customer            # quote must for the customer on the invoice
    ).update(invoice=id)

    Quote.objects.exclude(pk__in=quote_ids).filter(
        jobID__organization=org,  # Ensure the quote's job is linked to the user's organization
        invoice=id # find all quotes linked to this invoice
    ).update(invoice=None)
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
    """gets all the data for invoice detailed view"""
    org = request.org
    invoice_qs = Invoice.objects.filter(
        customer__organization=org.pk,
        pk = id
        )
    if not invoice_qs.exists():
        return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    res = invoice_qs[0].json_for_view_invoice()

    res_quotes = []

    quotes = Quote.objects.filter(invoice=id)
    aggregated_values = quotes.aggregate(
        total_material_subtotal=Sum("material_subtotal"),
        total_total_price=Sum("total_price"),
    )
    total_discnt = Decimal(0)

    for quote in quotes:
        total_discnt += quote.discount_type.discount_percent if quote.discount_type else Decimal(0)
        res_quotes.append(quote.jsonToDisplayForInvoice())

    total_discnt = total_discnt/len(quotes)
    aggregated_subtotal = aggregated_values["total_total_price"] or 0

    res["quotes"] = {
        "quotes": res_quotes,
        "totalMaterialSubtotal": str(aggregated_values["total_material_subtotal"] or 0),
        "subtotal": str(aggregated_subtotal),
        "taxPercent": str(invoice_qs[0].tax),
        "totalDiscount": str(total_discnt), # this is agregated from the discounts, eg 0.3 (30%)
        # total_discnt is like 30.05%, i know the casting is disgusting, sorry -alex
        "grandtotal" : str((aggregated_subtotal * (Decimal(f"0.{str(100 - total_discnt).replace('.', '')}"))) * (1 + invoice_qs[0].tax))
    }

    return Response(res, status=status.HTTP_200_OK)