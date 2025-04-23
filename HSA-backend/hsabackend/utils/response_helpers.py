from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from models.contractor import Contractor
from models.customer import Customer
from models.invoice import Invoice
from models.job import Job
from models.job_template import JobTemplate
from models.material import Material
from models.request import Request
from models.service import Service
from serializers.contractor_serializer import ContractorSerializer
from serializers.customer_serializer import CustomerSerializer
from serializers.invoice_serializer import InvoiceSerializer
from serializers.job_serializer import JobSerializer
from serializers.job_template_serializer import JobTemplateSerializer
from serializers.material_serializer import MaterialSerializer
from serializers.request_serializer import RequestSerializer
from serializers.service_serializer import ServiceSerializer


def get_table_data(request, object_type):
    org = request.org
    search = request.query_params.get('search', '')
    pagesize = request.query_params.get('pagesize', '')
    offset = request.query_params.get('offset', 0) * pagesize

    if not pagesize or not offset:
        return Response(


        data = {
            "message": "missing pagesize or offset"
        },
        status = status.HTTP_400_BAD_REQUEST
        )
    try:
        pagesize = int(pagesize)
        offset = int(offset)
    except:
        return Response(
        data = {
            "message": "pagesize and offset must be int"
        },
        status = status.HTTP_400_BAD_REQUEST
        )

    match object_type:
        case "job_template":
            job_templates = JobTemplate.objects.filter(organization=org.pk).filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )[offset:offset + pagesize] if search else JobTemplate.objects.filter(organization=org.pk)[offset:offset + pagesize]

            serializer = JobTemplateSerializer(job_templates, many=True)

            count = JobTemplate.objects.filter(organization=org.pk).filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            ).count() if search else JobTemplate.objects.filter(organization=org.pk).count()
        case "contractor":
            contractors = Contractor.objects.filter(organization=org.pk).filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )[offset:offset + pagesize] if search else Contractor.objects.filter(organization=org.pk)[offset:offset + pagesize]

            serializer = ContractorSerializer(contractors, many=True)

            count = Contractor.objects.filter(organization=org.pk).filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search)
            ).count() if search else Contractor.objects.filter(organization=org.pk).count()
        case "customer":
            customers = Customer.objects.filter(organization=org.pk).filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )[offset:offset + pagesize] if search else Customer.objects.filter(organization=org.pk)[offset:offset + pagesize]

            serializer = CustomerSerializer(customers, many=True)

            count = Customer.objects.filter(organization=org.pk).filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search)
            ).count() if search else Customer.objects.filter(organization=org.pk).count()
        case "job":
            jobs = Job.objects.filter(organization=org.pk).filter(
                Q(customer__first_name__icontains=search) |
                Q(customer__last_name__icontains=search) |
                Q(start_date__icontains=search) |
                Q(end_date__icontains=search) |
                Q(job_status__icontains=search) |
                Q(description__icontains=search)
            )[offset:offset + pagesize] if search else Job.objects.filter(organization=org.pk)[offset:offset + pagesize]

            serializer = JobSerializer(jobs, many=True)

            count = Job.objects.filter(organization=org.pk).filter(
                Q(customer__first_name__icontains=search) |
                Q(customer__last_name__icontains=search) |
                Q(start_date__icontains=search) |
                Q(end_date__icontains=search) |
                Q(job_status__icontains=search) |
                Q(description__icontains=search)
            ).count() if search else Job.objects.filter(organization=org.pk).count()
        case "service":
            services = Service.objects.filter(organization=org.pk).filter(
                Q(service_name__icontains=search) |
                Q(service_description__icontains=search) |
                Q(default_fee__icontains=search)
            )[offset:offset + pagesize] if search else Service.objects.filter(organization=org.pk).filter()
            serializer = ServiceSerializer(services, many=True)
            count = Service.objects.filter(organization=org.pk).filter(
                Q(service_name__icontains=search) |
                Q(service_description__icontains=search) |
                Q(default_fee__icontains=search)
            ).count() if search else Service.objects.filter(organization=org.pk).count()
        case "material":
            materials = Material.objects.filter(organization=org.pk).filter(
                Q(material_name__icontains=search)
            )[offset:offset + pagesize] if search else Material.objects.filter(organization=org.pk)[offset:offset + pagesize]

            serializer = MaterialSerializer(materials, many=True)

            count = Material.objects.filter(organization=org.pk).filter(
                Q(material_name__icontains=search)
            ).count() if search else Material.objects.filter(organization=org.pk).count()

        case "request":
            requests = Request.objects.filter(organization=org.pk).filter(
                Q(name__icontains=search))[offset:offset + pagesize] if search else Request.objects.filter(
                organization=org.pk)[offset:offset + pagesize]

            serializer = RequestSerializer(requests, many=True)

            count = Request.objects.filter(organization=org.pk).filter(
                Q(name__icontains=search)).count() if search else Request.objects.filter(
                organization=org.pk).count()
        case "invoice":
            invoices = Invoice.objects.filter(organization=org.pk).filter(
                Q(date_issued__icontains=search) |
                Q(date_due__icontains=search) |
                Q(status__icontains=search) |
                Q(customer__first_name__icontains=search) |
                Q(customer__last_name__icontains=search) |
                Q(payment_link__icontains=search) |
                Q(sales_tax_percent__icontains=search) |
                Q(discount__discount_name__icontains=search) |
                Q(discount__discount_percent__icontains=search)
            )[offset:offset + pagesize] if search else Invoice.objects.filter(organization=org.pk)[offset:offset + pagesize]
            serializer = InvoiceSerializer(invoices, many=True)
            count = Invoice.objects.filter(organization=org.pk).filter(
                Q(date_issued__icontains=search) |
                Q(date_due__icontains=search) |
                Q(status__icontains=search) |
                Q(customer__first_name__icontains=search) |
                Q(customer__last_name__icontains=search) |
                Q(payment_link__icontains=search) |
                Q(sales_tax_percent__icontains=search) |
                Q(discount__discount_name__icontains=search) |
                Q(discount__discount_percent__icontains=search
            )).count() if search else Invoice.objects.filter(organization=org.pk).count()
        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    res = {
        'data': serializer.data,
        'totalCount': count
    }
    return Response(res, status=status.HTTP_200_OK)