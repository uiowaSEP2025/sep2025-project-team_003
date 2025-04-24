from django.db.models import Q
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from hsabackend.models.booking import Booking
from hsabackend.models.contractor import Contractor
from hsabackend.models.customer import Customer
from hsabackend.models.invoice import Invoice
from hsabackend.models.job import Job
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.material import Material
from hsabackend.models.request import Request
from hsabackend.models.service import Service
from hsabackend.serializers.booking_serializer import BookingSerializer
from hsabackend.serializers.contractor_serializer import ContractorSerializer
from hsabackend.serializers.customer_serializer import CustomerSerializer
from hsabackend.serializers.invoice_serializer import InvoiceSerializer
from hsabackend.serializers.job_contractor_serializer import JobContractorSerializer
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


def get_table_data(request, object_type, exclude=False):
    org = request.org
    search = request.query_params.get('search', '')
    paginator = CustomPagination()

    if exclude:
        exclude_ids = [int(excluded_id) for excluded_id in request.GET.getlist('excludeIDs', [])]

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
                Q(requester_first_name__icontains=search) |
                Q(requester_last_name__icontains=search) |
                Q(requester_email__icontains=search) |
                Q(requester_city__icontains=search) |
                Q(requester_state__icontains=search) |
                Q(requester_zip__icontains=search) |
                Q(requester_address__icontains=search) |
                Q(requester_phone__icontains=search) |
                Q(description__icontains=search) |
                Q(availability__icontains=search) |
                Q(request_status__icontains=search) |
                Q(organization__icontains=search) |
                Q(job__icontains=search)
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
        case "booking":
            queryset = Booking.objects.filter(organization=org.pk)
            if search:
                queryset = queryset.filter(
                    Q(job__customer__first_name__icontains=search) |
                    Q(job__customer__last_name__icontains=search) |
                    Q(job__start_date__icontains=search) |
                    Q(job__end_date__icontains=search) |
                    Q(job__job_status__icontains=search) |
                    Q(job__description__icontains=search) |
                    Q(event_name__icontains=search) |
                    Q(start_time__icontains=search) |
                    Q(end_time__icontains=search) |
                    Q(booking_type__icontains=search) |
                    Q(status__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = BookingSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

def get_individual_data(request, object_id, object_type):
    org = request.org
    match object_type:
        case "job_template":
            try:
                query = JobTemplate.objects.get(pk=object_id, organization=org)
            except JobTemplate.DoesNotExist:
                return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = JobTemplateSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)

        case "contractor":
            try:
                query = Contractor.objects.get(pk=object_id, organization=org)
            except Contractor.DoesNotExist:
                return Response({"message": "The contractor does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The contractor does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ContractorSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "customer":
            try:
                query = Customer.objects.get(pk=object_id, organization=org)
            except Customer.DoesNotExist:
                return Response({"message": "The customer does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The customer does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CustomerSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "job":
            try:
                query = Job.objects.get(pk=object_id, organization=org)
            except Job.DoesNotExist:
                return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = JobSerializer(query)

            return Response(serializer.data, status=status.HTTP_200_OK)
        case "service":
            try:
                query = Service.objects.get(pk=object_id, organization=org)
            except Service.DoesNotExist:
                return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ServiceSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)

        case "material":
            try:
                query = Material.objects.get(pk=object_id, organization=org)
            except Material.DoesNotExist:
                return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = MaterialSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)

        case "request":
            try:
                query = Request.objects.get(pk=object_id, organization=org)
            except Request.DoesNotExist:
                return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = RequestSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "invoice":
            try:
                query = Invoice.objects.get(pk=object_id, organization=org)
            except Invoice.DoesNotExist:
                return Response({"message": "The invoice does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The invoice does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = InvoiceSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "booking":
            try:
                query = Booking.objects.get(pk=object_id, organization=org)
            except Booking.DoesNotExist:
                return Response({"message": "The booking does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The booking does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = BookingSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

def create_individual_data(request, object_type):
    org = request.org
    match object_type:
        case "job_template":
            serializer = JobTemplateSerializer(data=request.data)
        case "contractor":
            serializer = ContractorSerializer(data=request.data)
        case "customer":
            serializer = CustomerSerializer(data=request.data)
        case "job":
            serializer = JobSerializer(data=request.data)
        case "service":
            serializer = ServiceSerializer(data=request.data)
        case "material":
            serializer = MaterialSerializer(data=request.data)
        case "request":
            serializer = RequestSerializer(data=request.data)
        case "invoice":
            serializer = InvoiceSerializer(data=request.data)
        case "booking":
            serializer = BookingSerializer(data=request.data)
        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    if serializer.is_valid():
        serializer.save(organization=org)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_individual_data(request, object_id, object_type):
    org = request.org
    match object_type:
        case "job_template":
            query_object = JobTemplate.filter(organization=org.pk, pk=object_id).first()
            serializer = JobTemplateSerializer(query_object, data=request.data)
        case "contractor":
            query_object = Contractor.filter(organization=org.pk, pk=object_id).first()
            serializer = ContractorSerializer(query_object, data=request.data)
        case "customer":
            query_object = Customer.filter(organization=org.pk, pk=object_id).first()
            serializer = CustomerSerializer(query_object, data=request.data)
        case "job":
            query_object = Job.filter(organization=org.pk, pk=object_id).first()
            serializer = JobSerializer(query_object, data=request.data)
        case "service":
            query_object = Service.filter(organization=org.pk, pk=object_id).first()
            serializer = ServiceSerializer(query_object, data=request.data)
        case "material":
            query_object = Material.filter(organization=org.pk, pk=object_id).first()
            serializer = MaterialSerializer(query_object, data=request.data)
        case "request":
            query_object = Request.filter(organization=org.pk, pk=object_id).first()
            serializer = RequestSerializer(query_object, data=request.data)
        case "invoice":
            query_object = Invoice.filter(organization=org.pk, pk=object_id).first()
            serializer = InvoiceSerializer(query_object, data=request.data)
        case "booking":
            query_object = Booking.filter(organization=org.pk, pk=object_id).first()
            serializer = BookingSerializer(query_object, data=request.data)
        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    if serializer.is_valid():
        serializer.update(query_object, request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_object(request, object_id, object_type):
    org = request.org
    match object_type:
        case "job_template":
            query_object = JobTemplate.filter(organization=org.pk, pk=object_id).first()
        case "contractor":
            query_object = Contractor.filter(organization=org.pk, pk=object_id).first()
        case "customer":
            query_object = Customer.filter(organization=org.pk, pk=object_id).first()
        case "job":
            query_object = Job.filter(organization=org.pk, pk=object_id).first()
        case "service":
            query_object = Service.filter(organization=org.pk, pk=object_id).first()
        case "material":
            query_object = Material.filter(organization=org.pk, pk=object_id).first()
        case "request":
            query_object = Request.filter(organization=org.pk, pk=object_id).first()
        case "invoice":
            query_object = Invoice.filter(organization=org.pk, pk=object_id).first()
        case "booking":
            query_object = Booking.filter(organization=org.pk, pk=object_id).first()
        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    query_object.delete()
    return Response({
        "message": object_type + " deleted successfully"
    }, status=status.HTTP_200_OK)