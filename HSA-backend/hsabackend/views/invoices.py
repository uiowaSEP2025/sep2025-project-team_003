from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.customer import Customer 
from hsabackend.models.invoice import Invoice
from django.db.transaction import atomic
from django.core.exceptions import ValidationError
from django.db.models import Q
from hsabackend.models.job import Job
from hsabackend.utils.api_validators import parseAndReturnDate, parse_and_return_decimal
from django.db.transaction import atomic
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from decimal import Decimal

@api_view(["POST"])
@check_authenticated_and_onboarded()
def createInvoice(request):
    json = request.data  
    org = request.org

    customer_id = json.get("customerID", None)
    job_ids = json.get("jobIds",[])
    if not isinstance(customer_id, int):
        return Response({"message": "CustomerID must be int"}, status=status.HTTP_400_BAD_REQUEST)  
    
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

    try:
        with atomic():
            invoice = Invoice(
                customer = cust_qs[0],
                issuance_date = issued,
                due_date = due,
                tax = parse_and_return_decimal(tax_percent),
                status=invoice_status)
        
            invoice.full_clean()
            invoice.save()

            Job.objects.filter(organization=org.pk, job_status="completed",
                        invoice=None, customer=cust_qs[0]).update(invoice=invoice.pk)

    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"error": "500"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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

    job_ids = json.get("jobIds",[])

    if not isinstance(job_ids, list):
        return Response({"message": "Jobs must be list"}, status=status.HTTP_400_BAD_REQUEST)  
    
    if len(job_ids) == 0:
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
    
    try: 
        with atomic():
            invoice = invoice_qs[0]
            invoice.status = invoice_status
            invoice.issuance_date = issued
            invoice.due_date = due
            invoice.tax = parse_and_return_decimal(tax_percent)
            invoice.full_clean()
            invoice.save()

            Job.objects.filter(customer=invoice.customer).filter(Q(invoice=None) | Q(invoice=invoice)).update(invoice=invoice)

    except ValidationError as e:
        return Response({"errors": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"errors": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
    
    inv = invoice_qs[0]

    res = inv.json_for_view_invoice()

    res_jobs = []

    jobs = Job.objects.filter(invoice=id)
    
    total = Decimal(0)
    for job in jobs:
        tmp = job.get_finances()
        tmp["description"] = job.truncated_job_desc
        res_jobs.append(tmp)
        total += job.total_cost

    tax_percent = (inv.tax * Decimal('0.01'))
    tax_amount = total * tax_percent

    decimal_tax_amount = Decimal(str(round(tax_amount, 2)))
    decimal_tax_percent = Decimal(str(round(tax_percent, 2)))

    res["taxAmount"] = str(decimal_tax_amount)
    res["taxPercent"] = str(round(inv.tax, 2))
    res["grandTotal"] = str(round(decimal_tax_amount + total, 2))
    res["jobs"] = res_jobs


    return Response(res, status=status.HTTP_200_OK)