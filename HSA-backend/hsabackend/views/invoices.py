from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.customer import Customer 
from hsabackend.models.quote import Quote
from hsabackend.models.invoice import Invoice
from hsabackend.models.organization import Organization
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from django.db.models import Sum
from hsabackend.utils.api_validators import parseAndReturnDate

@api_view(["POST"])
def createInvoice(request):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    json = request.data  
    org = Organization.objects.get(owning_User=request.user.pk)

    customer_id = json.get("customerID", None)
    quote_ids = json.get("quoteIDs",[])
    if not isinstance(customer_id, int):
        return Response({"message": "CustomerID must be int"}, status=status.HTTP_400_BAD_REQUEST)  
    
    if not isinstance(quote_ids, list):
        return Response({"message": "Quotes must be list"}, status=status.HTTP_400_BAD_REQUEST)  
    
    if len(quote_ids) == 0:
        return Response({"message": "Must include at least 1 quote"}, status=status.HTTP_400_BAD_REQUEST)  

    cust_qs = Customer.objects.filter(pk=int(customer_id), organization=org)

    if not cust_qs.exists():
        # will be here if user does not own the customer ID
        return Response({"message": "Must provide customer for the invoice."}, status=status.HTTP_404_NOT_FOUND)

    invoice = Invoice(
        customer = cust_qs[0],
        issuance_date = timezone.now()
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
def getInvoices(request):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    org = Organization.objects.get(owning_User=request.user.pk)
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
def updateInvoice(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    org = Organization.objects.get(owning_User=request.user.pk)
    json = request.data  

    quote_ids = json.get("quoteIDs",[])

    if not isinstance(quote_ids, list):
        return Response({"message": "Quotes must be list"}, status=status.HTTP_400_BAD_REQUEST)  
    
    if len(quote_ids) == 0:
        return Response({"message": "Must include at least 1 quote"}, status=status.HTTP_400_BAD_REQUEST)  

    invoice_status = json.get("status",None)
    issued = json.get("issuedDate",None)
    due = json.get("dueDate",None)

    if not invoice_status or invoice_status not in ('created', 'issued', 'paid'):
        return Response({"message": "Must include a valid status 'created' | 'issued' | 'paid'"}, status=status.HTTP_400_BAD_REQUEST)  

    if invoice_status != 'created' and (not issued or not not due):
        return Response({"message": "Must include issuance and due dates"}, status=status.HTTP_400_BAD_REQUEST)  

    if invoice_status != 'created':
        issuance = parseAndReturnDate(issued)
        due = parseAndReturnDate(due)
        if not issuance or not due:
            return Response({"message": f"Must provide a valid {'issuance' if issuance == None else 'due'} date"}, status=status.HTTP_400_BAD_REQUEST)  
        if due < issuance:
            return Response({"message": "Due date can not be before the issuance date"}, status=status.HTTP_400_BAD_REQUEST)  
        

    invoice_qs = Invoice.objects.filter(
        customer__organization=org.pk,
        pk = id
        )
    
    if not invoice_qs.exists():
        return Response({"message": "The invoice does not exist"}, status=status.HTTP_404_NOT_FOUND)
    customer = invoice_qs[0].customer

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
def deleteInvoice(request,id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    org = Organization.objects.get(owning_User=request.user.pk)
    invoice_qs = Invoice.objects.filter(
        customer__organization=org.pk,
        pk = id
        )
    if not invoice_qs.exists():
        return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)
    invoice_qs[0].delete()
    return Response({"message": "Invoice Deleted successfully"}, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_data_for_invoice(request, id):
    """gets all the data for invoice detailed view"""
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    org = Organization.objects.get(owning_User=request.user.pk)
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


    for quote in quotes:
        res_quotes.append(quote.jsonToDisplayForInvoice())

    
    res["quotes"] = {
        "quotes": res_quotes,
        "totalMaterialSubtotal": aggregated_values["total_material_subtotal"] or 0,
        "totalPrice": aggregated_values["total_total_price"] or 0,
    }

    
    return Response(res, status=status.HTTP_200_OK)
