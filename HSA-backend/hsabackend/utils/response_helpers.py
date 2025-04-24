from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from hsabackend.models.contractor import Contractor
from hsabackend.models.customer import Customer
from hsabackend.models.invoice import Invoice
from hsabackend.models.job import Job
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.material import Material
from hsabackend.models.request import Request
from hsabackend.models.service import Service
from hsabackend.serializers.contractor_serializer import ContractorSerializer
from hsabackend.serializers.customer_serializer import CustomerSerializer
from hsabackend.serializers.invoice_serializer import InvoiceSerializer
from hsabackend.serializers.job_serializer import JobSerializer
from hsabackend.serializers.job_template_serializer import JobTemplateSerializer
from hsabackend.serializers.material_serializer import MaterialSerializer
from hsabackend.serializers.request_serializer import RequestSerializer
from hsabackend.serializers.service_serializer import ServiceSerializer


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'pagesize'
    page_query_param = 'offset'

    def get_page_number(self, request, paginator):
        # Get the page number from the request
        page_number = request.query_params.get(self.page_query_param, 0)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            # In the original implementation, offset is 0-indexed
            # Django's pagination is 1-indexed, so we add 1
            return int(page_number) + 1
        except (TypeError, ValueError):
            return 1

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'totalCount': self.page.paginator.count
        })


def get_table_data(request, object_type, exclude=False, exclude_ids=None):
    org = request.org
    search = request.query_params.get('search', '')
    paginator = CustomPagination()

    match object_type:
        case "job_template":
            queryset = JobTemplate.objects.filter(organization=org.pk)
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(description__icontains=search)
                )

            page = paginator.paginate_queryset(queryset, request)
            serializer = JobTemplateSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "contractor":
            queryset = Contractor.objects.filter(organization=org.pk)
            if search:
                queryset = queryset.filter(
                    Q(first_name__icontains=search) | Q(last_name__icontains=search)
                )

            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])

            page = paginator.paginate_queryset(queryset, request)
            serializer = ContractorSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "customer":
            queryset = Customer.objects.filter(organization=org.pk)
            if search:
                queryset = queryset.filter(
                    Q(first_name__icontains=search) | Q(last_name__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = CustomerSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "job":
            queryset = Job.objects.filter(organization=org.pk)
            if search:
                queryset = queryset.filter(
                    Q(customer__first_name__icontains=search) |
                    Q(customer__last_name__icontains=search) |
                    Q(start_date__icontains=search) |
                    Q(end_date__icontains=search) |
                    Q(job_status__icontains=search) |
                    Q(description__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = JobSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "service":
            queryset = Service.objects.filter(organization=org.pk)
            if search:
                queryset = queryset.filter(
                    Q(service_name__icontains=search) |
                    Q(service_description__icontains=search) |
                    Q(default_fee__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = ServiceSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "material":
            queryset = Material.objects.filter(organization=org.pk)
            if search:
                queryset = queryset.filter(
                    Q(material_name__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = MaterialSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        case "request":
            queryset = Request.objects.filter(organization=org.pk)
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = RequestSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "invoice":
            queryset = Invoice.objects.filter(organization=org.pk)
            if search:
                queryset = queryset.filter(
                    Q(date_issued__icontains=search) |
                    Q(date_due__icontains=search) |
                    Q(status__icontains=search) |
                    Q(customer__first_name__icontains=search) |
                    Q(customer__last_name__icontains=search) |
                    Q(payment_link__icontains=search) |
                    Q(sales_tax_percent__icontains=search) |
                    Q(discount__discount_name__icontains=search) |
                    Q(discount__discount_percent__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = InvoiceSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
